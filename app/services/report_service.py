from pathlib import Path
from datetime import datetime
import textwrap
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from app.services.metrics_service import (
    fetch_total_revenue,
    fetch_top_customers,
    fetch_top_products,
    fetch_total_orders,
    fetch_average_order_value,
)

# Function that builds both markdown and PDF sales reports for the last 7 days
def build_sales_report() -> dict:
    # Fetch total revenue 
    revenue = fetch_total_revenue(days=7)
    # Fetch top 3 customers 
    customers = fetch_top_customers(limit=3, days=7)
    # Fetch top 3 products 
    products = fetch_top_products(limit=3, days=7)
    # Fetch number of completed orders 
    total_orders = fetch_total_orders(days=7)
    # Fetch average order value 
    average_order_value = fetch_average_order_value(days=7)
    # Get top customer name 
    top_customer = customers[0]["customer_name"] if customers else "N/A"
    # Get top customer spending 
    top_customer_spent = customers[0]["total_spent"] if customers else 0
    # Build customer lines for the markdown report 
    customer_lines = "\n".join(
        [f"- {customer['customer_name']}: ${customer['total_spent']:,.2f}" for customer in customers]
    ) if customers else "- N/A"

    # Build product lines for the markdown report
    product_lines = "\n".join(
        [f"- {product['product_name']}: ${product['product_revenue']:,.2f}" for product in products]
    ) if products else "- N/A"

    # Create a Path object for the reports directory
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # Generate timestamp for each report
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Build report path
    markdown_path = reports_dir / f"weekly_sales_report_{timestamp}.md"

    # Build the full report  using fetched metrics
    report_text = textwrap.dedent(
        f"""
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
        """
    ).strip()

    # Write text to the markdown file
    markdown_path.write_text(report_text, encoding="utf-8")

    # Build PDF file path
    pdf_path = markdown_path.with_suffix(".pdf")

    # Create document object pointing to the PDF path
    doc = SimpleDocTemplate(str(pdf_path))

    # Load stylesheet for headings and text
    styles = getSampleStyleSheet()

    # Create a list to hold PDF elements
    elements = []

    # Loop each line of the markdown text to convert it into PDF 
    for line in report_text.split("\n"):
        # Remove whitespace from the current line
        line = line.strip()
        if not line:
            # Add vertical space to the PDF for blank lines
            elements.append(Spacer(1, 10))
            continue
        if line.startswith("# "):
            # Add the text as PDF Heading  1
            elements.append(Paragraph(line[2:], styles["Heading1"]))
        # Check whether the line is level 2  heading
        elif line.startswith("## "):
            # Add the text as a PDF Heading 2 element
            elements.append(Paragraph(line[3:], styles["Heading2"]))
        # Check whether the line is a markdown bullet point
        elif line.startswith("- "):
            # Add the text as a normal paragraph with a bullet symbol
            elements.append(Paragraph("• " + line[2:], styles["Normal"]))
        else:
            # Add text as a normal paragraph
            elements.append(Paragraph(line, styles["Normal"]))

        # Add spacing line for readability in the PDF
        elements.append(Spacer(1, 10))

    # Build the final PDF file 
    doc.build(elements)

    # Return both output file paths 
    return {
        "markdown_path": str(markdown_path),
        "pdf_path": str(pdf_path),
    }