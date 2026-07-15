from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from slack_sdk import WebClient
from agents import Runner
from agents.mcp import MCPServerStdio, MCPServerStdioParams
from dotenv import load_dotenv
import os
import re
import time
import hmac
import hashlib
import logging
from app.services.report_service import build_sales_report
from app.agent import create_operations_agent
from app.services.operations_report_service import build_operations_report

# Configure basic logging for the application
logging.basicConfig(level=logging.INFO)

load_dotenv()

# Set to track processed Slack event IDs and avoid duplicate handling
processed_event_ids = set()

# Dictionary to store pending report paths by Slack channel until approval
pending_reports = {}

# Dictionary to store Slack user who requested the pending report
pending_report_users = {}

# Dictionary to store the report label (sales vs operations) for the pending report
pending_report_labels = {}

# Create Slack client 
slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

# Define the request body schema for the /run-agent endpoint
class AgentRequest(BaseModel):
    # Store user prompt that will be sent to the agent
    prompt: str

# Define an application lifespan handler so MCP starts once when FastAPI starts and closes on shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the MCP server configuration
    params = MCPServerStdioParams(
        command="python",
        args=["-m", "app.mcp_server"],
    )

    # Create MCP stdio client with tool list 
    server = MCPServerStdio(
        # Pass stdio server startup parameters
        params=params,

        # Cache MCP tool list 
        cache_tools_list=True,

        # Server internal name
        name="operations-mcp",
    )

    # Open MCP server connection for the FastAPI app lifetime
    async with server:
        # Store the connected MCP server on the FastAPI app state so routes can access it
        app.state.mcp_server = server

        # Yield control back to FastAPI while the app is running
        yield


# Create the FastAPI application and attach the lifespan handler
app = FastAPI(
    # Set the title shown in FastAPI docs
    title="AI Operations Agent",

    # Register the startup and shutdown lifecycle handler
    lifespan=lifespan,
)


# Define a helper function that verifies Slack request signatures
def verify_slack_signature(request_body: bytes, timestamp: str, slack_signature: str) -> bool:
    # Read the Slack signing secret from environment variables
    signing_secret = os.getenv("SLACK_SIGNING_SECRET")

    # Return false immediately if any required value is missing
    if not signing_secret or not timestamp or not slack_signature:
        return False

    # Reject old requests to help prevent replay attacks
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    # Build Slack's required signature base string from version, timestamp, and raw request body
    sig_basestring = f"v0:{timestamp}:{request_body.decode('utf-8')}"

    # Compute the expected Slack signature using HMAC SHA256
    computed_signature = "v0=" + hmac.new(
        signing_secret.encode("utf-8"),
        sig_basestring.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    # Compare the computed signature against the incoming Slack signature securely
    return hmac.compare_digest(computed_signature, slack_signature)


# Define a helper function that builds the agent using the connected MCP server
def get_agent() -> object:
    # Read the connected MCP server from FastAPI application state
    server = app.state.mcp_server

    # Build and return the operations agent wired to that MCP server
    return create_operations_agent(server)


# Define the root health-check endpoint
@app.get("/")
async def root():
    # Return a simple confirmation message showing the API is running
    return {"message": "AI Operations Agent API is running with MCP"}


# Define an endpoint for manually running the agent with a prompt
@app.post("/run-agent")
async def run_agent(request: AgentRequest):
    # Build the MCP-connected agent
    agent = get_agent()

    # Run the agent with the user prompt
    result = await Runner.run(agent, request.prompt)

    # Return the final agent output
    return {"response": result.final_output}

# Define an endpoint to directly generate the weekly procurement/operations report
@app.post("/generate-operations-report")
async def generate_operations_report():
    paths = build_operations_report()

    return {
        "message": "Weekly operations report generated successfully",
        "markdown_path": paths["markdown_path"],
        "pdf_path": paths["pdf_path"],
    }

# Define an endpoint for directly generating the weekly report without going through the agent
@app.post("/generate-report")
async def generate_report():
    # Build the markdown and PDF report files
    paths = build_sales_report()

    # Return the generated file paths
    return {
        "message": "Weekly report generated successfully",
        "markdown_path": paths["markdown_path"],
        "pdf_path": paths["pdf_path"],
    }


# Define the Slack Events API endpoint so Slack can send mentions and verification payloads
@app.post("/slack/events")
async def slack_events(request: Request):
    # Read the raw request body because Slack signature verification must use the exact raw bytes
    raw_body = await request.body()

    # Parse the request JSON payload
    payload = await request.json()

    # Log that a Slack event was received
    logging.info("Slack event received")

    # Log the Slack payload for debugging
    logging.info(f"Slack payload: {payload}")

    # Handle Slack URL verification during app setup by echoing the challenge value
    if payload.get("type") == "url_verification":
        return JSONResponse(content={"challenge": payload["challenge"]})

    # Read the Slack signature header from the request
    slack_signature = request.headers.get("x-slack-signature")

    # Read the Slack timestamp header from the request
    slack_timestamp = request.headers.get("x-slack-request-timestamp")

    # Reject the request if Slack signature verification fails
    if not verify_slack_signature(raw_body, slack_timestamp, slack_signature):
        raise HTTPException(status_code=403, detail="Invalid Slack signature")

    # Extract the top-level Slack event ID
    event_id = payload.get("event_id")

    # Ignore duplicate events that were already processed earlier
    if event_id in processed_event_ids:
        return {"ok": True}

    # Save the event ID so future duplicates are ignored
    if event_id:
        processed_event_ids.add(event_id)

    # Continue only for normal Slack event callback payloads
    if payload.get("type") == "event_callback":
        # Extract the inner Slack event object
        event = payload.get("event", {})

        # Ignore bot messages to avoid reply loops
        if event.get("subtype") == "bot_message":
            return {"ok": True}

        # Handle app mentions where a user tags the bot
        if event.get("type") == "app_mention":
            try:
                # Extract the original message text
                text = event.get("text", "")

                # Extract the Slack channel ID
                channel = event.get("channel")

                # Extract the Slack user ID
                user_id = event.get("user")

                # Remove the bot mention token from the message and trim whitespace
                cleaned_text = re.sub(r"<@[^>]+>\s*", "", text).strip()

                # Create a lowercase version for command matching
                cleaned_text_lower = cleaned_text.lower()

                # If the user only mentioned the bot, ask for a real request
                if not cleaned_text:
                    slack_client.chat_postMessage(
                        channel=channel,
                        text="Please include a request, e.g. 'generate weekly KPI report'",
                    )
                    return {"ok": True}

                # Handle approval replies by uploading the pending report PDF for that Slack channel
                if cleaned_text_lower == "approve":
                    # Check whether there is a pending report for this channel
                    if channel not in pending_reports:
                        # Tell the user there is nothing waiting for approval
                        slack_client.chat_postMessage(
                            channel=channel,
                            text="There is no pending report to approve.",
                        )
                        return {"ok": True}

                    # Check whether the same user who requested the report is approving it
                    if pending_report_users.get(channel) != user_id:
                        # Tell the user only the requester can approve
                        slack_client.chat_postMessage(
                            channel=channel,
                            text="Only the user who requested the report can approve it.",
                        )
                        return {"ok": True}

                    # Read the stored report paths for this channel
                    paths = pending_reports.pop(channel)

                    # Remove the stored requesting user for this channel
                    pending_report_users.pop(channel, None)

                    # Remove the stored report label for this channel
                    report_label = pending_report_labels.pop(channel, "Weekly KPI Report")

                    # Upload the PDF report to Slack with a short approval message
                    slack_client.files_upload_v2(
                        file=paths["pdf_path"],
                        title=report_label,
                        channel=channel,
                        initial_comment=(
                            f"Approved {report_label.lower()} upload.\n"
                            f"Markdown: {paths['markdown_path']}"
                        ),
                    )
                    return {"ok": True}

                # Handle flexible weekly report generation requests inside Slack
                if "generate" in cleaned_text_lower and "weekly" in cleaned_text_lower and "report" in cleaned_text_lower:
                    # Build the operations report if the request mentions operations or procurement
                    if "operations" in cleaned_text_lower or "procurement" in cleaned_text_lower:
                        paths = build_operations_report()
                        report_label = "Weekly Operations Report"
                    else:
                        paths = build_sales_report()
                        report_label = "Weekly KPI Report"

                    # Save the generated report paths until approval
                    pending_reports[channel] = paths

                    # Save the Slack user who requested the report
                    pending_report_users[channel] = user_id

                    # Save the report label for this channel
                    pending_report_labels[channel] = report_label

                    # Send a Slack message telling the user the report is ready and awaiting approval
                    slack_client.chat_postMessage(
                        channel=channel,
                        text=(
                            f"{report_label} is ready.\n"
                            f"Markdown: {paths['markdown_path']}\n"
                            "Reply with approve to upload the PDF."
                        ),
                    )
                    return {"ok": True}

                # Build the MCP-connected agent for all other Slack requests
                agent = get_agent()

                # Run the agent on the cleaned Slack message text
                result = await Runner.run(agent, cleaned_text)

                # Send the agent's final response back to the same Slack channel
                slack_client.chat_postMessage(
                    channel=channel,
                    text=result.final_output,
                )

            # Catch any unexpected error while processing the Slack event
            except Exception as e:
                # Log the error details
                logging.exception("Slack event error")

                # Send the error message back to Slack when a channel is available
                if event.get("channel"):
                    slack_client.chat_postMessage(
                        channel=event["channel"],
                        text=f"Error: {str(e)}",
                    )

    # Return a success acknowledgment to Slack
    return {"ok": True}


# python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
# python -m streamlit run app/dashboard.py --server.port 8501 --server.address 0.0.0.0
# ./.venv/bin/python -m streamlit run app/dashboard.py --server.port 8501 --server.address 0.0.0.0