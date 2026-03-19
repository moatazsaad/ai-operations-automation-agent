from agents import function_tool

@function_tool
def send_slack_report_notification(report_path: str) -> str:
    message = f"""
Weekly Sales Report Generated

Report:
{report_path}
"""

    return message.strip()