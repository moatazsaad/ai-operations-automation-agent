from mcp.server.fastmcp import FastMCP
from app.services.metrics_service import (
    fetch_total_revenue,
    fetch_top_customers,
    fetch_top_products,
    fetch_total_orders,
    fetch_average_order_value,
)

from app.services.procurement_metrics_service import (
    fetch_low_stock_items,
    fetch_delayed_purchase_orders,
    fetch_supplier_performance,
    fetch_procurement_spend_by_supplier,
    fetch_reorder_recommendations,
    fetch_top_delayed_suppliers,
)
from app.services.operations_report_service import build_operations_report
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

# MCP tool to get delayed purchase orders
@mcp.tool()
def get_delayed_purchase_orders() -> list:
    """
    Returns purchase orders marked as delayed.
    """
    return fetch_delayed_purchase_orders()

# Tool for checking inventory items that need reorder
@mcp.tool()
def get_low_stock_items() -> list:
    return fetch_low_stock_items()


@mcp.tool()
def get_supplier_performance() -> list:
    return fetch_supplier_performance()

@mcp.tool()
def get_procurement_spend_by_supplier() -> list:
    return fetch_procurement_spend_by_supplier()

@mcp.tool()
def generate_operations_report() -> dict:
    return build_operations_report()

@mcp.tool()
def get_reorder_recommendations() -> list:
    return fetch_reorder_recommendations()

@mcp.tool()
def get_top_delayed_suppliers() -> list:
    """
    Returns suppliers ranked by delay severity.
    The result is already sorted by delayed PO count, average days delayed, and max days delayed.
    Do not reorder the result.
    """
    return fetch_top_delayed_suppliers()

if __name__ == "__main__":
    mcp.run()
    
    # uv run uvicorn app.main:app --reload --port 8000
    """curl -X POST http://127.0.0.1:8001/run-agent \
    -H "Content-Type: application/json" \
    -d '{"prompt":"Show me low stock items that need reorder"}'"""
    
    """curl -s -X POST http://127.0.0.1:8001/run-agent \
-H "Content-Type: application/json" \
-d '{"prompt":"Generate weekly operations report"}'"""