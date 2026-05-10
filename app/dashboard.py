import streamlit as st
import pandas as pd

from app.services.procurement_metrics_service import (
    fetch_low_stock_items,
    fetch_delayed_purchase_orders,
    fetch_supplier_performance,
    fetch_procurement_spend_by_supplier,
    fetch_reorder_recommendations,
)

from app.services.operations_report_service import build_operations_report


st.set_page_config(
    page_title="AI Procurement Control Tower",
    layout="wide",
)

st.title("AI Procurement Control Tower")
st.caption("AI-powered procurement visibility, supplier performance, inventory risk, and operational reporting")

# Load data
low_stock_items = fetch_low_stock_items()
delayed_orders = fetch_delayed_purchase_orders()
supplier_performance = fetch_supplier_performance()
spend_by_supplier = fetch_procurement_spend_by_supplier()
reorder_recommendations = fetch_reorder_recommendations()

# DataFrames
low_stock_df = pd.DataFrame(low_stock_items)
delayed_df = pd.DataFrame(delayed_orders)
supplier_df = pd.DataFrame(supplier_performance)
spend_df = pd.DataFrame(spend_by_supplier)
reorder_df = pd.DataFrame(reorder_recommendations)

# KPI values
total_spend = sum(item["total_spend"] for item in spend_by_supplier)

avg_on_time = (
    sum(item["on_time_delivery_rate"] for item in supplier_performance)
    / len(supplier_performance)
    if supplier_performance
    else 0
)

# KPI cards
st.subheader("Executive Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Low-Stock Items", len(low_stock_items))
col2.metric("Delayed POs", len(delayed_orders))
col3.metric("Reorder Recommendations", len(reorder_recommendations))
col4.metric("Total Procurement Spend", f"${total_spend:,.2f}")
col5.metric("Avg On-Time Rate", f"{avg_on_time:.2f}%")

st.divider()

# AI insights
st.subheader("AI Insights")

insights = []

if delayed_orders:
    insights.append(f"{len(delayed_orders)} purchase order(s) are delayed and may need supplier follow-up.")

if low_stock_items:
    insights.append(f"{len(low_stock_items)} item(s) are below reorder point and may create inventory risk.")

if spend_by_supplier:
    top_supplier = spend_by_supplier[0]
    insights.append(
        f"{top_supplier['supplier_name']} has the highest procurement spend at ${top_supplier['total_spend']:,.2f}."
    )

if supplier_performance:
    risky_supplier = supplier_performance[0]
    insights.append(
        f"{risky_supplier['supplier_name']} should be reviewed due to supplier performance risk."
    )

if not insights:
    insights.append("No major procurement risks detected at this time.")

for insight in insights:
    st.info(insight)

st.divider()

# Recommended actions
st.subheader("Recommended Actions")

actions = []

for item in reorder_recommendations:
    actions.append(
        f"Reorder {item['recommended_order_quantity']} units of {item['item_name']}."
    )

for order in delayed_orders:
    actions.append(
        f"Follow up with {order['supplier_name']} for delayed PO #{order['purchase_order_id']}."
    )

if supplier_performance:
    actions.append("Review supplier scorecard and prioritize suppliers with delays or low on-time rate.")

if not actions:
    actions.append("No urgent action required.")

for action in actions:
    st.success(action)

st.divider()

# Charts
st.subheader("Procurement Analytics")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("Spend by Supplier")
    if not spend_df.empty:
        st.bar_chart(spend_df.set_index("supplier_name")["total_spend"])
    else:
        st.info("No spend data available.")

with chart_col2:
    st.write("Supplier On-Time Delivery Rate")
    if not supplier_df.empty:
        st.bar_chart(supplier_df.set_index("supplier_name")["on_time_delivery_rate"])
    else:
        st.info("No supplier data available.")

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.write("Delayed Purchase Orders by Supplier")
    if not supplier_df.empty:
        st.bar_chart(supplier_df.set_index("supplier_name")["delayed_purchase_orders"])
    else:
        st.info("No delay data available.")

with chart_col4:
    st.write("Inventory Risk by Item")
    if not reorder_df.empty:
        st.bar_chart(reorder_df.set_index("item_name")["recommended_order_quantity"])
    else:
        st.info("No reorder data available.")

st.divider()

# Tables
st.subheader("Detailed Procurement Data")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Reorder Recommendations",
        "Low Stock",
        "Delayed POs",
        "Supplier Performance",
        "Spend by Supplier",
    ]
)

with tab1:
    if not reorder_df.empty:
        st.dataframe(reorder_df, use_container_width=True)
    else:
        st.success("No reorder recommendations.")

with tab2:
    if not low_stock_df.empty:
        st.dataframe(low_stock_df, use_container_width=True)
    else:
        st.success("No low-stock items.")

with tab3:
    if not delayed_df.empty:
        st.dataframe(delayed_df, use_container_width=True)
    else:
        st.success("No delayed purchase orders.")

with tab4:
    if not supplier_df.empty:
        st.dataframe(supplier_df, use_container_width=True)
    else:
        st.info("No supplier performance data.")

with tab5:
    if not spend_df.empty:
        st.dataframe(spend_df, use_container_width=True)
    else:
        st.info("No spend data.")

st.divider()

# Report generation
st.subheader("Executive Report Generation")

if st.button("Generate Weekly Operations Report"):
    paths = build_operations_report()

    st.success("Weekly operations report generated successfully.")
    st.write(f"Markdown: {paths['markdown_path']}")
    st.write(f"PDF: {paths['pdf_path']}")