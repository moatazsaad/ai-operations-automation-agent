from agents import Agent
from agents.extensions.models.litellm_model import LitellmModel
from app.tools.database_tools import (
    get_total_revenue,        
    get_top_customers,        
    get_top_products,         
    get_total_orders,         
    get_average_order_value,  
)
from app.tools.report_tools import generate_sales_report
from app.tools.email_tools import draft_sales_report_email

model = LitellmModel(
    model="huggingface/openai/gpt-oss-20b:fireworks-ai"
)

agent = Agent(
    name="operations_agent",
    instructions="""
    You are an operations analyst for a company.

    Rules:
    - Use tools for business data questions.
    - If asked to generate or save a sales report, call generate_sales_report.
    - Do not invent numbers, file paths, or actions you did not take.
    - Do not say that you posted to Slack or sent a Slack notification.
    - Just return the result of the report generation clearly and concisely.
    """,
    model=model,
    tools=[
        get_total_revenue,
        get_top_customers,
        get_top_products,
        get_total_orders,
        get_average_order_value,
        generate_sales_report,
        draft_sales_report_email,
    ]
)