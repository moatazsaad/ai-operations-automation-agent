from pathlib import Path
from agents import function_tool

# Build email message
def build_email_draft(report_path: str) -> str:
    
    email_text = f"""
Subject: Weekly Sales Report

Hello Leadership Team,

The weekly sales report has been generated.

You can find the report here:
{report_path}

Please review the results and let me know if further analysis is needed.

Best,
Operations Analytics
"""
    emails_dir = Path("reports")
    emails_dir.mkdir(exist_ok=True)

    email_file = emails_dir / "weekly_report_email.txt"

    email_file.write_text(email_text.strip(), encoding="utf-8")

    return str(email_file)

@function_tool
def draft_sales_report_email(report_path: str) -> str:
    path = build_email_draft(report_path)
    return f"Email draft saved to {path}"