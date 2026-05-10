# Run by cron to generate and upload the weekly operations report to Slack automatically
from app.services.operations_report_service import build_operations_report
from slack_sdk import WebClient
from dotenv import load_dotenv
import os

load_dotenv()

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

if __name__ == "__main__":
    paths = build_operations_report()
    pdf_path = paths["pdf_path"]
    markdown_path = paths["markdown_path"]

    client.files_upload_v2(
        file=pdf_path,
        title="Weekly Operations Report",
        channel="C0ALWKNQ3PV",
        initial_comment=(
            f"Weekly operations report generated.\n"
            f"Markdown: {markdown_path}"
        ),
    )

    print(f"Uploaded to Slack: {pdf_path}")
    
    # python -m app.run_weekly_operations_report