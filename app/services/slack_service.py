# Function that builds a Slack notification message for a generated report
def build_slack_report_notification(report_path: str) -> str:
    # Build and return the Slack message text including the report path
    return f"""
Weekly Sales Report Generated

Report:
{report_path}
""".strip()