# Import FastAPI main framework class, Request object for incoming HTTP requests, and HTTPException for returning HTTP errors
from fastapi import FastAPI, Request, HTTPException

# Import JSONResponse to manually return JSON responses when needed
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from slack_sdk import WebClient
from agents import Runner
from dotenv import load_dotenv
import os
import re
import time
# Import hmac for secure Slack signature verification
import hmac
# Import hashlib to compute SHA256 hash for Slack signature verification
import hashlib
# Import the configured AI agent
from app.agent import agent
from app.tools.report_tools import build_sales_report
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

app = FastAPI(title="AI Operations Agent")

# Store processed Slack event IDs to avoid handling duplicate events
processed_event_ids = set()

# Store pending generated reports by Slack channel until user approves upload
pending_reports = {}

# Create Slack client 
slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

# Define request body schema for /run-agent endpoint
class AgentRequest(BaseModel):
    # The text prompt that will be sent to the agent
    prompt: str

# Verify that the Slack request really came from Slack using request body, timestamp, and signature
def verify_slack_signature(request_body: bytes, timestamp: str, slack_signature: str) -> bool:
    # Read Slack signing secret from environment variables
    signing_secret = os.getenv("SLACK_SIGNING_SECRET")

    # If any required value is missing, reject the request
    if not signing_secret or not timestamp or not slack_signature:
        return False

    # Reject request if timestamp is older than 5 minutes to prevent replay attacks
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    # Build Slack signature base string in required format: version:timestamp:raw_body
    sig_basestring = f"v0:{timestamp}:{request_body.decode('utf-8')}"

    # Compute expected signature using HMAC SHA256 with Slack signing secret
    computed_signature = "v0=" + hmac.new(
        signing_secret.encode("utf-8"),
        sig_basestring.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    # Safely compare computed signature with Slack-provided signature
    return hmac.compare_digest(computed_signature, slack_signature)


# Root endpoint to confirm API is running
@app.get("/")
async def root():
    return {"message": "AI Operations Agent API is running"}

# Endpoint to run the agent manually 
@app.post("/run-agent")
async def run_agent(request: AgentRequest):
    result = await Runner.run(agent, request.prompt)

    return {"response": result.final_output}

# Endpoint to generate sales report 
@app.post("/generate-report")
async def generate_report():
    # Build markdown and PDF sales report
    paths = build_sales_report()

    # Return generated file paths
    return {
        "message": "Weekly report generated successfully",
        "markdown_path": paths["markdown_path"],
        "pdf_path": paths["pdf_path"],
    }

# Slack Events API endpoint to receive Slack events such as bot mentions
@app.post("/slack/events")
async def slack_events(request: Request):
    raw_body = await request.body()
    # Parse request body as JSON payload
    payload = await request.json()

    logging.info("Slack event received")
    logging.info(f"Slack payload: {payload}")

    # Handle Slack URL verification challenge during Slack app setup
    if payload.get("type") == "url_verification":
        return JSONResponse(content={"challenge": payload["challenge"]})

    # Read Slack signature header from request
    slack_signature = request.headers.get("x-slack-signature")

    # Read Slack timestamp header from request
    slack_timestamp = request.headers.get("x-slack-request-timestamp")

    # Reject request if Slack signature verification fails
    if not verify_slack_signature(raw_body, slack_timestamp, slack_signature):
        raise HTTPException(status_code=403, detail="Invalid Slack signature")

    # Extract unique Slack event ID
    event_id = payload.get("event_id")
    
    # Ignore duplicate events if already processed
    if event_id in processed_event_ids:
        print("Duplicate event ignored:", event_id)
        return {"ok": True}

    # Save event ID after first processing
    if event_id:
        processed_event_ids.add(event_id)

    # Process normal Slack event callback payload
    if payload.get("type") == "event_callback":
        # Extract actual event object from payload
        event = payload.get("event", {})

        # Ignore bot messages to avoid loops where bot replies trigger itself again
        if event.get("subtype") == "bot_message":
            return {"ok": True}

        # Process app mention events (when user mentions the bot in Slack)
        if event.get("type") == "app_mention":
            try:
                # Debug print when mention is received
                print("Received mention")

                # Extract original message text from event
                text = event.get("text", "")

                # Extract Slack channel ID where message was sent
                channel = event.get("channel")

                # Remove bot mention tag like <@BOTID> from text and trim spaces
                cleaned_text = re.sub(r"<@[^>]+>\s*", "", text).strip()

                # Lowercase cleaned text for easier command matching
                cleaned_text_lower = cleaned_text.lower()

                # Debug print cleaned user message
                print("Cleaned text:", cleaned_text)

                # If user only mentioned bot without request, ask for a valid request
                if not cleaned_text:
                    slack_client.chat_postMessage(
                        channel=channel,
                        text="Please include a request, e.g. 'generate weekly KPI report'"
                    )
                    return {"ok": True}

                # If user replies with "approve", upload the pending report PDF for that channel
                if cleaned_text_lower == "approve":
                    # Check whether a pending report exists for this channel
                    if channel in pending_reports:
                        # Get and remove saved pending report paths
                        paths = pending_reports.pop(channel)

                        # Upload PDF file to Slack with initial comment
                        slack_client.files_upload_v2(
                            file=paths["pdf_path"],
                            title="Weekly KPI Report",
                            channel=channel,
                            initial_comment=(
                                "Approved weekly KPI report upload.\n"
                                f"Markdown: {paths['markdown_path']}"
                            ),
                        )
                        # Debug print after successful PDF upload
                        print("Approved PDF uploaded to Slack")
                    else:
                        # Inform user if no report is waiting for approval
                        slack_client.chat_postMessage(
                            channel=channel,
                            text="There is no pending report to approve."
                        )
                    return {"ok": True}

                # If user asks to generate weekly KPI/sales report, build it and wait for approval
                if "generate weekly kpi report" in cleaned_text_lower or "generate weekly sales report" in cleaned_text_lower:
                    # Generate report files
                    paths = build_sales_report()

                    # Save generated report paths until user approves PDF upload
                    pending_reports[channel] = paths

                    # Send Slack message with markdown path and approval instruction
                    slack_client.chat_postMessage(
                        channel=channel,
                        text=(
                            "Weekly KPI report is ready.\n"
                            f"Markdown: {paths['markdown_path']}\n"
                            "Reply with *approve* to upload the PDF."
                        )
                    )
                    # Debug print after report generation
                    print("Report generated and waiting for approval")
                    return {"ok": True}

                # For any other mention, run the AI agent on the cleaned user text
                result = await Runner.run(agent, cleaned_text)

                # Debug print agent response
                print("After agent:", result.final_output)

                # Send agent response back to the same Slack channel
                slack_client.chat_postMessage(
                    channel=channel,
                    text=result.final_output
                )

                # Debug print after sending Slack message
                print("Message sent to Slack")

            except Exception as e:
                # Print any error that occurs while processing Slack event
                print("Slack event error:", str(e))

                # If channel exists, send error message back to Slack
                if event.get("channel"):
                    slack_client.chat_postMessage(
                        channel=event["channel"],
                        text=f"Error: {str(e)}"
                    )

    # Return ok response to Slack so it knows event was received successfully
    return {"ok": True}