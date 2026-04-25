from pathlib import Path
# Function to build and save an email draft for report
def build_email_draft(report_path: str) -> str:
    # Create email body text and insert the report path into it
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

    # Create path for the reports directory where the email draft file will be saved
    emails_dir = Path("reports")
    emails_dir.mkdir(exist_ok=True)
    email_file = emails_dir / "weekly_report_email.txt"
    email_file.write_text(email_text.strip(), encoding="utf-8")
    return str(email_file)