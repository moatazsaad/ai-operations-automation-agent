from mcp.server.fastmcp import FastMCP
from app.services.metrics_service import (
    fetch_total_revenue,
    fetch_top_customers,
    fetch_top_products,
    fetch_total_orders,
    fetch_average_order_value,
)
from app.services.report_service import build_sales_report
from app.services.email_service import build_email_draft

# Create MCP server 
mcp = FastMCP("operations-mcp")

# Register function as an MCP tool 
@mcp.tool()
def get_total_revenue(days: int | None = None) -> float:
    return fetch_total_revenue(days)

@mcp.tool()
def get_top_customers(limit: int = 3, days: int | None = None) -> list:
    return fetch_top_customers(limit, days)

@mcp.tool()
def get_top_products(limit: int = 3, days: int | None = None) -> list:
    return fetch_top_products(limit, days)

@mcp.tool()
def get_total_orders(days: int | None = None) -> int:
    return fetch_total_orders(days)

@mcp.tool()
def get_average_order_value(days: int | None = None) -> float:
    return fetch_average_order_value(days)

@mcp.tool()
def generate_sales_report() -> dict:
    return build_sales_report()

@mcp.tool()
def draft_sales_report_email(report_path: str) -> str:
    return build_email_draft(report_path)


if __name__ == "__main__":
    mcp.run()