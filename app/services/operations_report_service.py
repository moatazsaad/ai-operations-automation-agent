from pathlib import Path
from datetime import datetime
import textwrap

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from app.services.procurement_metrics_service import (
    fetch_low_stock_items,
    fetch_delayed_purchase_orders,
    fetch_supplier_performance,
    fetch_procurement_spend_by_supplier,
)


def build_operations_report() -> dict:
    low_stock_items = fetch_low_stock_items()
    delayed_orders = fetch_delayed_purchase_orders()
    supplier_performance = fetch_supplier_performance()
    spend_by_supplier = fetch_procurement_spend_by_supplier()

    low_stock_lines = "\n".join(
        [
            f"- {item['item_name']} ({item['category']}): "
            f"{item['current_stock']} in stock, reorder point {item['reorder_point']}"
            for item in low_stock_items
        ]
    ) if low_stock_items else "- No low stock items"

    delayed_order_lines = "\n".join(
        [
            f"- PO #{order['purchase_order_id']} - {order['item_name']} "
            f"from {order['supplier_name']}, expected {order['expected_delivery_date']}"
            for order in delayed_orders
        ]
    ) if delayed_orders else "- No delayed purchase orders"

    supplier_lines = "\n".join(
        [
            f"- {supplier['supplier_name']}: "
            f"{supplier['delayed_purchase_orders']} delayed POs, "
            f"{supplier['on_time_delivery_rate']}% on-time delivery rate, "
            f"${supplier['total_spend']:,.2f} spend"
            for supplier in supplier_performance
        ]
    ) if supplier_performance else "- No supplier data"

    spend_lines = "\n".join(
        [
            f"- {supplier['supplier_name']}: ${supplier['total_spend']:,.2f}"
            for supplier in spend_by_supplier
        ]
    ) if spend_by_supplier else "- No spend data"

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    markdown_path = reports_dir / f"weekly_operations_report_{timestamp}.md"

    report_text = textwrap.dedent(
        f"""
        # Weekly Operations Report

        ## Executive Summary
        This report summarizes procurement, inventory, supplier performance, and purchasing spend.
        Current risk areas include {len(low_stock_items)} low-stock items and {len(delayed_orders)} delayed purchase orders.

        ## Inventory Risks
        {low_stock_lines}

        ## Delayed Purchase Orders
        {delayed_order_lines}

        ## Supplier Performance
        {supplier_lines}

        ## Procurement Spend by Supplier
        {spend_lines}
        """
    ).strip()

    markdown_path.write_text(report_text, encoding="utf-8")

    pdf_path = markdown_path.with_suffix(".pdf")
    doc = SimpleDocTemplate(str(pdf_path))
    styles = getSampleStyleSheet()
    elements = []

    for line in report_text.split("\n"):
        line = line.strip()

        if not line:
            elements.append(Spacer(1, 10))
            continue

        if line.startswith("# "):
            elements.append(Paragraph(line[2:], styles["Heading1"]))
        elif line.startswith("## "):
            elements.append(Paragraph(line[3:], styles["Heading2"]))
        elif line.startswith("- "):
            elements.append(Paragraph("• " + line[2:], styles["Normal"]))
        else:
            elements.append(Paragraph(line, styles["Normal"]))

        elements.append(Spacer(1, 10))

    doc.build(elements)

    return {
        "markdown_path": str(markdown_path),
        "pdf_path": str(pdf_path),
    }
    
    # python -c "from app.services.operations_report_service import build_operations_report; print(build_operations_report())"