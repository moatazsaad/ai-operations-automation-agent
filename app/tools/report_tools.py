from pathlib import Path
from agents import function_tool
from app.tools.database_tools import (
    fetch_total_revenue,
    fetch_top_customers,
    fetch_top_products,
    fetch_total_orders,
    fetch_average_order_value,
)
import textwrap
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# Build sales report (Markdown + PDF)
def build_sales_report() -> dict:

    # Fetch key business metrics from database
    revenue = fetch_total_revenue(days=7)                  # total revenue from completed orders
    customers = fetch_top_customers(3, days=7)             # top 3 customers by spending
    products = fetch_top_products(3, days=7)               # top 3 products by revenue
    total_orders = fetch_total_orders(days=7)              # total number of completed orders
    average_order_value = fetch_average_order_value(days=7)  # average order value
    
    top_customer = customers[0]['customer_name'] if customers else "N/A"
    top_customer_spent = customers[0]['total_spent'] if customers else 0

    # Format top products into bullets for report
    product_lines = "\n".join(
        [f"- {p['product_name']}: ${p['product_revenue']:,.2f}" for p in products]
    ) if products else "- N/A"

    # Create "reports" directory 
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # Generate timestamp to create unique report file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Define markdown file path
    report_path = reports_dir / f"weekly_sales_report_{timestamp}.md"

    # Format top customers into bullets for report
    customer_lines = "\n".join(
        [f"- {c['customer_name']}: ${c['total_spent']:,.2f}" for c in customers]
    ) if customers else "- N/A"

    # Build the markdown report 
    report_text = textwrap.dedent(f"""
# Weekly Sales Report

## Executive Summary
This week, total completed-order revenue was ${revenue:,.2f}.
The company completed {total_orders} orders with an average order value of ${average_order_value:,.2f}.
The top customer was {top_customer} with ${top_customer_spent:,.2f} in purchases.

## Key Metrics
- Total Revenue: ${revenue:,.2f}
- Total Orders: {total_orders}
- Average Order Value: ${average_order_value:,.2f}

## Top Customers
{customer_lines}

## Top Products
{product_lines}
""")

    # Write markdown report to file
    report_path.write_text(report_text, encoding="utf-8")

    # Create PDF file path with same name
    pdf_path = report_path.with_suffix(".pdf")

    # Create PDF document object
    doc = SimpleDocTemplate(str(pdf_path))

    # Load default styles for formatting text in PDF
    styles = getSampleStyleSheet()

    # List to store PDF elements 
    elements = []

    # Convert markdown text into PDF elements line by line
    for line in report_text.split("\n"):
        line = line.strip()  

        # If line is empty, add spacing
        if not line:
            elements.append(Spacer(1, 10))
            continue

        # If line is main title (#)
        if line.startswith("# "):
            elements.append(Paragraph(line[2:], styles["Heading1"]))

        # If line is section title (##)
        elif line.startswith("## "):
            elements.append(Paragraph(line[3:], styles["Heading2"]))

        # If line is bullet point (-)
        elif line.startswith("- "):
            elements.append(Paragraph("• " + line[2:], styles["Normal"]))

        # Otherwise normal paragraph text
        else:
            elements.append(Paragraph(line, styles["Normal"]))

        # Add spacing after each element
        elements.append(Spacer(1, 10))

    # Build PDF document from elements
    doc.build(elements)

    # Return file paths for markdown and PDF reports
    return {
    "markdown_path": str(report_path),
    "pdf_path": str(pdf_path),
}

# Expose report generation as a tool 
@function_tool
def generate_sales_report() -> str:

    # Call main report builder function
    paths = build_sales_report()

    # Return message with saved file locations
    return f"Report saved to {paths['markdown_path']} and {paths['pdf_path']}"