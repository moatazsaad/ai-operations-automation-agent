from app.database.db import get_connection

# Function to fetch total revenue from completed orders
def fetch_total_revenue(days: int | None = None) -> float:

    conn = get_connection()
    cursor = conn.cursor()

    # Query for completed orders revenue
    query = """
        SELECT SUM(total_amount)
        FROM orders
        WHERE status = 'completed'
    """

    # List to hold SQL parameters
    params = []

    # Date filter 
    if days is not None:
        # Extend query to include rows from the given number of days
        query += " AND order_date >= CURRENT_DATE - (%s * INTERVAL '1 day')"

        # Add days value
        params.append(days)

    # Execute query with the parameters
    cursor.execute(query, tuple(params))

    # Read the first row and column returned by the query
    revenue = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    
    # Return result or 0 if database returned null
    return float(revenue or 0)


# Function to fetch top customers by spending
def fetch_top_customers(limit: int = 3, days: int | None = None) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    # Query joining orders to customers
    query = """
        SELECT c.name, SUM(o.total_amount) AS total_spent
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        WHERE o.status = 'completed'
    """

    # List to hold SQL parameters
    params = []

    # Date filter
    if days is not None:
        # Extend query to include rows from the given number of days
        query += " AND o.order_date >= CURRENT_DATE - (%s * INTERVAL '1 day')"

        # Add days value
        params.append(days)

    # Add grouping, sorting and limiting to return the top customers
    query += """
        GROUP BY c.name
        ORDER BY total_spent DESC
        LIMIT %s
    """

    # Add days value
    params.append(limit)

    # Execute the query with the parameters
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()

    # Convert each database row into Python dictionary
    return [
        {
            "customer_name": row[0],
            "total_spent": float(row[1]),
        }
        for row in rows
    ]

# Function to fetch top products by revenue
def fetch_top_products(limit: int = 3, days: int | None = None) -> list:
    
    conn = get_connection()
    cursor = conn.cursor()

    # Query joining orders to products
    query = """
        SELECT p.name, SUM(o.total_amount) AS product_revenue
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.status = 'completed'
    """

    params = []

    if days is not None:
        query += " AND o.order_date >= CURRENT_DATE - (%s * INTERVAL '1 day')"
        params.append(days)

    # Add grouping, sorting, and limiting to return the top products
    query += """
        GROUP BY p.name
        ORDER BY product_revenue DESC
        LIMIT %s
    """
    params.append(limit)
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        {
            "product_name": row[0],
            "product_revenue": float(row[1]),
        }
        for row in rows
    ]


# Function to count completed orders
def fetch_total_orders(days: int | None = None) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    # Query for counting completed orders
    query = """
        SELECT COUNT(*)
        FROM orders
        WHERE status = 'completed'
    """
    params = []
    if days is not None:
        query += " AND order_date >= CURRENT_DATE - (%s * INTERVAL '1 day')"
        params.append(days)

    cursor.execute(query, tuple(params))
    total_orders = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return int(total_orders or 0)


# Function to compute the average order value for completed orders
def fetch_average_order_value(days: int | None = None) -> float:

    conn = get_connection()
    cursor = conn.cursor()

    # Query for average completed order value
    query = """
        SELECT AVG(total_amount)
        FROM orders
        WHERE status = 'completed'
    """
    params = []
    if days is not None:
        query += " AND order_date >= CURRENT_DATE - (%s * INTERVAL '1 day')"
        params.append(days)

    cursor.execute(query, tuple(params))
    avg_order_value = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    return float(avg_order_value or 0)