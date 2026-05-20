import os
import requests
import streamlit as st
import pandas as pd
from app.services.procurement_metrics_service import (
    fetch_low_stock_items,
    fetch_delayed_purchase_orders,
    fetch_supplier_performance,
    fetch_procurement_spend_by_supplier,
    fetch_reorder_recommendations,
    fetch_top_delayed_suppliers,
)
from app.services.operations_report_service import build_operations_report


# Page Configuration

# Configure the browser tab title and dashboard layout
st.set_page_config(
    page_title="AI Procurement Control Tower",
    layout="wide",
)


# Convert raw database-style column names into clean business-friendly names
# Example: purchase_order_id -> Purchase Order ID
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()

    df.columns = [
        col.replace("_", " ")
        .title()
        .replace("Po", "PO")
        .replace("Id", "ID")
        .replace("Url", "URL")
        for col in df.columns
    ]

    return df


# Format money values for display
def format_money(value: float) -> str:
    return f"${value:,.2f}"


# Dashboard Header

# Main dashboard title
st.title("AI Procurement Control Tower")

# Short dashboard description
st.caption(
    "AI-powered procurement visibility, supplier performance, inventory risk, and operational reporting"
)

st.divider()


# Ask AI Agent Section

# Section title for natural-language interaction
st.subheader("Ask the AI Operations Agent")

# Read the FastAPI backend URL from environment variables
# If FASTAPI_URL is not set, the dashboard uses local FastAPI
api_url = os.getenv("FASTAPI_URL", "http://localhost:8000")

# Create two columns: one for input, one for example questions
agent_col1, agent_col2 = st.columns([2, 1])

with agent_col1:
    # Text area where the user asks a natural-language question
    user_prompt = st.text_area(
        "Ask a procurement, inventory, supplier, sales, or reporting question:",
        placeholder="Example: Show me top delayed suppliers by average days delayed",
        height=120,
    )

    # Button to send the user question to the FastAPI agent endpoint
    ask_button = st.button("Ask Agent", type="primary")

with agent_col2:
    # Show example prompts to make the UI easier to demo
    st.markdown("Suggested demo questions")
    st.code(
        "Show me delayed purchase orders\n"
        "Show me top delayed suppliers by average days delayed\n"
        "Show me low stock items\n"
        "Give me reorder recommendations\n"
        "Generate weekly operations report",
        language="text",
    )

# Handle Ask Agent button click
if ask_button:
    # Validate that the user entered a question
    if not user_prompt.strip():
        st.warning("Please enter a question.")
    else:
        try:
            # Send the user question to FastAPI /run-agent
            response = requests.post(
                f"{api_url}/run-agent",
                json={"prompt": user_prompt},
                timeout=90,
            )

            # If the backend returns success, display the agent answer
            if response.status_code == 200:
                agent_response = response.json().get("response", "No response returned.")

                st.markdown("#### Agent Response")
                st.info(agent_response)

            # If the backend returns an error, show the error details
            else:
                st.error(f"API error: {response.status_code}")
                st.write(response.text)

        # Handle connection errors or timeout errors
        except Exception as e:
            st.error(f"Could not connect to FastAPI: {e}")

st.divider()


# Load Data

# Fetch low-stock inventory items from PostgreSQL
low_stock_items = fetch_low_stock_items()

# Fetch delayed purchase orders from PostgreSQL
delayed_orders = fetch_delayed_purchase_orders()

# Fetch supplier performance metrics from PostgreSQL
supplier_performance = fetch_supplier_performance()

# Fetch procurement spend grouped by supplier
spend_by_supplier = fetch_procurement_spend_by_supplier()

# Fetch reorder recommendations for low-stock items
reorder_recommendations = fetch_reorder_recommendations()

# Fetch suppliers ranked by delay severity
# This includes delayed PO count, average days delayed, and max days delayed
top_delayed_suppliers = fetch_top_delayed_suppliers()


# Convert Data to DataFrames

# Convert list outputs into pandas DataFrames for Streamlit tables/charts
low_stock_df = pd.DataFrame(low_stock_items)
delayed_df = pd.DataFrame(delayed_orders)
supplier_df = pd.DataFrame(supplier_performance)
spend_df = pd.DataFrame(spend_by_supplier)
reorder_df = pd.DataFrame(reorder_recommendations)
top_delayed_suppliers_df = pd.DataFrame(top_delayed_suppliers)


# KPI Calculations

# Calculate total procurement spend across all suppliers
total_spend = sum(item["total_spend"] for item in spend_by_supplier)

# Calculate average supplier on-time delivery rate
# This is based on delivered POs only
avg_on_time = (
    sum(item["on_time_delivery_rate"] for item in supplier_performance)
    / len(supplier_performance)
    if supplier_performance
    else 0
)


# Executive KPI Cards

st.subheader("Executive Overview")

# Create KPI columns
col1, col2, col3, col4, col5 = st.columns(5)

# Display high-level executive metrics
col1.metric("Low-Stock Items", len(low_stock_items))
col2.metric("Delayed POs", len(delayed_orders))
col3.metric("Reorder Recommendations", len(reorder_recommendations))
col4.metric("Total Procurement Spend", format_money(total_spend))
col5.metric("Avg Delivered On-Time", f"{avg_on_time:.2f}%")

st.divider()


# AI Insights

st.subheader("AI Insights")

# Create an empty list to collect insight messages
insights = []

# Add insight if delayed purchase orders exist
if delayed_orders:
    insights.append(
        f"{len(delayed_orders)} purchase order(s) are delayed and may need supplier follow-up."
    )

# Add insight if low-stock items exist
if low_stock_items:
    insights.append(
        f"{len(low_stock_items)} item(s) are below reorder point and may create inventory risk."
    )

# Add insight for highest-spend supplier
if spend_by_supplier:
    top_supplier = spend_by_supplier[0]
    insights.append(
        f"{top_supplier['supplier_name']} has the highest procurement spend at "
        f"{format_money(top_supplier['total_spend'])}."
    )

# Add insight for supplier delay severity
if top_delayed_suppliers:
    worst_delay_supplier = top_delayed_suppliers[0]
    insights.append(
        f"{worst_delay_supplier['supplier_name']} is the top delayed supplier with "
        f"{worst_delay_supplier['delayed_po_count']} delayed POs, "
        f"{worst_delay_supplier['average_days_delayed']} average days delayed, "
        f"and {worst_delay_supplier['max_days_delayed']} max days delayed."
    )

# Add insight for supplier performance review
if supplier_performance:
    risky_supplier = supplier_performance[0]
    insights.append(
        f"{risky_supplier['supplier_name']} should be reviewed due to supplier performance risk."
    )

# If no risks are found, show a positive message
if not insights:
    insights.append("No major procurement risks detected at this time.")

# Display insights in columns for a cleaner layout
insight_cols = st.columns(2)

for index, insight in enumerate(insights):
    with insight_cols[index % 2]:
        st.info(insight)

st.divider()


# Recommended Actions

st.subheader("Recommended Actions")

# Create an empty list to collect recommended actions
actions = []

# Add reorder actions for low-stock items
for item in reorder_recommendations:
    actions.append(
        f"Reorder {item['recommended_order_quantity']} units of {item['item_name']}."
    )

# Add supplier follow-up actions for delayed purchase orders
for order in delayed_orders:
    actions.append(
        f"Follow up with {order['supplier_name']} for delayed PO #{order['purchase_order_id']}."
    )

# Add supplier delay review action using delay severity results
if top_delayed_suppliers:
    worst_delay_supplier = top_delayed_suppliers[0]
    actions.append(
        f"Prioritize supplier review for {worst_delay_supplier['supplier_name']} "
        f"because it has {worst_delay_supplier['delayed_po_count']} delayed POs."
    )

# Add supplier scorecard review action
if supplier_performance:
    actions.append(
        "Review supplier scorecard and prioritize suppliers with delays or low on-time rate."
    )

# Show a clean executive view instead of flooding the page
if not actions:
    st.success("No urgent action required.")
else:
    # Show only the first 8 actions on the main page
    for action in actions[:8]:
        st.success(action)

    # Hide the full action list inside an expander
    if len(actions) > 8:
        with st.expander(f"View all {len(actions)} recommended actions"):
            for action in actions:
                st.write(action)

st.divider()


# Procurement Analytics Charts

st.subheader("Procurement Analytics")

# Create two chart columns
chart_col1, chart_col2 = st.columns(2)

# Chart 1: Spend by supplier
with chart_col1:
    st.write("Spend by Supplier")
    if not spend_df.empty:
        st.bar_chart(spend_df.set_index("supplier_name")["total_spend"])
    else:
        st.info("No spend data available.")

# Chart 2: Delivered PO on-time rate by supplier
with chart_col2:
    st.write("Delivered PO On-Time Rate by Supplier")
    if not supplier_df.empty:
        st.bar_chart(supplier_df.set_index("supplier_name")["on_time_delivery_rate"])
    else:
        st.info("No supplier data available.")

# Create another two chart columns
chart_col3, chart_col4 = st.columns(2)

# Chart 3: Delayed purchase orders by supplier
with chart_col3:
    st.write("Delayed Purchase Orders by Supplier")
    if not supplier_df.empty:
        st.bar_chart(supplier_df.set_index("supplier_name")["delayed_purchase_orders"])
    else:
        st.info("No delay data available.")

# Chart 4: Inventory reorder risk by item
# The bar value is recommended_order_quantity
with chart_col4:
    st.write("Inventory Risk by Item")
    if not reorder_df.empty:
        st.bar_chart(reorder_df.set_index("item_name")["recommended_order_quantity"])
    else:
        st.info("No reorder data available.")

# Create another two chart columns for delay severity
chart_col5, chart_col6 = st.columns(2)

# Chart 5: Average days delayed by supplier
with chart_col5:
    st.write("Top Delayed Suppliers by Average Days Delayed")
    if not top_delayed_suppliers_df.empty:
        st.bar_chart(
            top_delayed_suppliers_df.set_index("supplier_name")["average_days_delayed"]
        )
    else:
        st.info("No delayed supplier severity data available.")

# Chart 6: Max days delayed by supplier
with chart_col6:
    st.write("Top Delayed Suppliers by Max Days Delayed")
    if not top_delayed_suppliers_df.empty:
        st.bar_chart(
            top_delayed_suppliers_df.set_index("supplier_name")["max_days_delayed"]
        )
    else:
        st.info("No delayed supplier severity data available.")

st.divider()


# Detailed Data Tables

st.subheader("Detailed Procurement Data")

# Create tabs for each detailed data section
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Reorder Recommendations",
        "Low Stock",
        "Delayed POs",
        "Supplier Performance",
        "Spend by Supplier",
        "Top Delayed Suppliers",
    ]
)

# Tab 1: Reorder recommendations
with tab1:
    if not reorder_df.empty:
        st.dataframe(clean_column_names(reorder_df), use_container_width=True)
    else:
        st.success("No reorder recommendations.")

# Tab 2: Low-stock items
with tab2:
    if not low_stock_df.empty:
        st.dataframe(clean_column_names(low_stock_df), use_container_width=True)
    else:
        st.success("No low-stock items.")

# Tab 3: Delayed purchase orders
with tab3:
    if not delayed_df.empty:
        st.dataframe(clean_column_names(delayed_df), use_container_width=True)
    else:
        st.success("No delayed purchase orders.")

# Tab 4: Supplier performance
with tab4:
    if not supplier_df.empty:
        st.dataframe(clean_column_names(supplier_df), use_container_width=True)
    else:
        st.info("No supplier performance data.")

# Tab 5: Procurement spend by supplier
with tab5:
    if not spend_df.empty:
        st.dataframe(clean_column_names(spend_df), use_container_width=True)
    else:
        st.info("No spend data.")

# Tab 6: Top delayed suppliers by delay severity
with tab6:
    if not top_delayed_suppliers_df.empty:
        st.dataframe(
            clean_column_names(top_delayed_suppliers_df),
            use_container_width=True,
        )
    else:
        st.info("No delayed supplier severity data.")

st.divider()


# Report Generation

st.subheader("Executive Report Generation")

# Button to generate the weekly operations report
if st.button("Generate Weekly Operations Report"):
    # Build Markdown and PDF report files
    paths = build_operations_report()

    # Show success message and generated file paths
    st.success("Weekly operations report generated successfully.")
    st.write(f"Markdown: {paths['markdown_path']}")
    st.write(f"PDF: {paths['pdf_path']}")
    
    # python -m streamlit run app/dashboard.py
    # default port is 8501