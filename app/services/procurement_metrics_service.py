# Import the database connection function from your database module
from app.database.db import get_connection


# Function to fetch inventory items where current stock is at or below reorder point
def fetch_low_stock_items() -> list:
    # Open a connection to the PostgreSQL database
    conn = get_connection()

    # Create a cursor to execute SQL queries
    cursor = conn.cursor()

    # SQL query to find items that need reorder
    query = """
        SELECT item_name, category, current_stock, reorder_point
        FROM inventory
        WHERE current_stock <= reorder_point
    """

    # Execute the SQL query
    cursor.execute(query)

    # Fetch all rows returned by the query
    rows = cursor.fetchall()

    # Close the cursor
    cursor.close()

    # Close the database connection
    conn.close()

    # Convert database rows into a list of dictionaries
    return [
        {
            "item_name": row[0],
            "category": row[1],
            "current_stock": row[2],
            "reorder_point": row[3],
        }
        for row in rows
    ]


# Function to fetch purchase orders that are marked as delayed
def fetch_delayed_purchase_orders() -> list:
    # Open a connection to the PostgreSQL database
    conn = get_connection()

    # Create a cursor to execute SQL queries
    cursor = conn.cursor()

    # SQL query to get delayed purchase orders with supplier name
    query = """
        SELECT po.id,
               s.name,
               po.item_name,
               po.expected_delivery_date,
               po.status
        FROM purchase_orders po
        JOIN suppliers s
        ON po.supplier_id = s.id
        WHERE po.actual_delivery_date IS NULL
        AND po.expected_delivery_date < CURRENT_DATE
    """

    # Execute the SQL query
    cursor.execute(query)

    # Fetch all rows returned by the query
    rows = cursor.fetchall()

    # Close the cursor
    cursor.close()

    # Close the database connection
    conn.close()

    # Convert database rows into a list of dictionaries
    return [
        {
            "purchase_order_id": row[0],
            "supplier_name": row[1],
            "item_name": row[2],
            "expected_delivery_date": str(row[3]),
            "status": "automatically_detected_delay",
        }
        for row in rows
    ]
    
    # Function to calculate supplier performance using purchase order data
def fetch_supplier_performance() -> list:
    # Open database connection
    conn = get_connection()

    # Create cursor to run SQL
    cursor = conn.cursor()

    # Calculate total POs, delayed POs, delivered POs, on-time delivered POs, and spend by supplier
    query = """
        SELECT
            s.name AS supplier_name,
            COUNT(po.id) AS total_purchase_orders,
            SUM(
                CASE
                    WHEN po.actual_delivery_date IS NULL
                    AND po.expected_delivery_date < CURRENT_DATE
                    THEN 1
                    ELSE 0
                END
            ) AS delayed_purchase_orders,
            SUM(
                CASE
                    WHEN po.actual_delivery_date IS NOT NULL
                    THEN 1
                    ELSE 0
                END
            ) AS delivered_purchase_orders,
            SUM(
                CASE
                    WHEN po.actual_delivery_date IS NOT NULL
                    AND po.actual_delivery_date <= po.expected_delivery_date
                    THEN 1
                    ELSE 0
                END
            ) AS on_time_deliveries,
            SUM(po.total_amount) AS total_spend
        FROM suppliers s
        LEFT JOIN purchase_orders po
        ON s.id = po.supplier_id
        GROUP BY s.name
        ORDER BY delayed_purchase_orders DESC, total_spend DESC
    """

    # Execute query
    cursor.execute(query)

    # Fetch rows
    rows = cursor.fetchall()

    # Close database resources
    cursor.close()
    conn.close()

    # Convert rows into dictionaries
    return [
        {
            "supplier_name": row[0],
            "total_purchase_orders": int(row[1] or 0),
            "delayed_purchase_orders": int(row[2] or 0),
            "delivered_purchase_orders": int(row[3] or 0),
            "on_time_deliveries": int(row[4] or 0),
            "total_spend": float(row[5] or 0),
            "on_time_delivery_rate": round(
                (int(row[4] or 0) / int(row[3] or 1)) * 100,
                2
            ),
        }
        for row in rows
    ]
    
    # Function to calculate procurement spend by supplier
def fetch_procurement_spend_by_supplier() -> list:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            s.name AS supplier_name,
            SUM(po.total_amount) AS total_spend
        FROM purchase_orders po
        JOIN suppliers s
        ON po.supplier_id = s.id
        GROUP BY s.name
        ORDER BY total_spend DESC
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "supplier_name": row[0],
            "total_spend": float(row[1] or 0),
        }
        for row in rows
    ]# Function to recommend reorder quantities for low-stock items
def fetch_reorder_recommendations() -> list:
    # Open database connection
    conn = get_connection()

    # Create cursor to execute SQL
    cursor = conn.cursor()

    # Find items at or below reorder point and calculate recommended quantity
    query = """
        SELECT
            item_name,
            category,
            current_stock,
            reorder_point,
            safety_stock,
            (reorder_point + safety_stock - current_stock) AS recommended_order_quantity
        FROM inventory
        WHERE current_stock <= reorder_point
    """

    # Execute query
    cursor.execute(query)

    # Fetch results
    rows = cursor.fetchall()

    # Close database resources
    cursor.close()
    conn.close()

    # Convert rows into dictionaries
    return [
        {
            "item_name": row[0],
            "category": row[1],
            "current_stock": row[2],
            "reorder_point": row[3],
            "safety_stock": row[4],
            "recommended_order_quantity": row[5],
        }
        for row in rows
    ]
    
    # testing
    # python -c "from app.services.procurement_metrics_service import fetch_low_stock_items; print(fetch_low_stock_items())"
    # python -c "from app.services.procurement_metrics_service import fetch_delayed_purchase_orders; print(fetch_delayed_purchase_orders())"
    # python -c "from app.services.procurement_metrics_service import fetch_supplier_performance; print(fetch_supplier_performance())"
    # python -c "from app.services.procurement_metrics_service import fetch_reorder_recommendations; print(fetch_reorder_recommendations())"
    # python -c "from app.services.procurement_metrics_service import fetch_procurement_spend_by_supplier; print(fetch_procurement_spend_by_supplier())"