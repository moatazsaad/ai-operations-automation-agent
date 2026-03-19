from app.tools.report_tools import build_sales_report
from slack_sdk import WebClient
from dotenv import load_dotenv
import os

load_dotenv()

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

if __name__ == "__main__":
    paths = build_sales_report()
    pdf_path = paths["pdf_path"]
    markdown_path = paths["markdown_path"]

    client.files_upload_v2(
        file=pdf_path,
        title="Weekly KPI Report",
        channel="C0ALWKNQ3PV",
        initial_comment=(
            f"Weekly KPI report generated.\n"
            f"Markdown: {markdown_path}"
        ),
    )

    print(f"Uploaded to Slack: {pdf_path}")