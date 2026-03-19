from agents import function_tool
from app.database.db import get_connection

# FETCH FUNCTIONS (DB LOGIC)

def fetch_total_revenue(days: int | None = None) -> float:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT SUM(total_amount)
        FROM orders
        WHERE status = 'completed'
    """
    params = []

    if days is not None:
        query += " AND order_date >= CURRENT_DATE - INTERVAL %s"
        params.append(f"{days} days")

    cursor.execute(query, tuple(params))

    revenue = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return float(revenue or 0)

def fetch_top_customers(limit: int = 3, days: int | None = None) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.name, SUM(o.total_amount) AS total_spent
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        WHERE o.status = 'completed'
    """
    params = []

    if days is not None:
        query += " AND o.order_date >= CURRENT_DATE - INTERVAL %s"
        params.append(f"{days} days")

    query += """
        GROUP BY c.name
        ORDER BY total_spent DESC
        LIMIT %s
    """
    params.append(limit)

    cursor.execute(query, tuple(params))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "customer_name": row[0],
            "total_spent": float(row[1])
        }
        for row in rows
    ]

def fetch_top_products(limit: int = 3, days: int | None = None) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT p.name, SUM(o.total_amount) AS product_revenue
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.status = 'completed'
    """
    params = []

    if days is not None:
        query += " AND o.order_date >= CURRENT_DATE - INTERVAL %s"
        params.append(f"{days} days")

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
            "product_revenue": float(row[1])
        }
        for row in rows
    ]

def fetch_total_orders(days: int | None = None) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT COUNT(*)
        FROM orders
        WHERE status = 'completed'
    """
    params = []

    if days is not None:
        query += " AND order_date >= CURRENT_DATE - INTERVAL %s"
        params.append(f"{days} days")

    cursor.execute(query, tuple(params))

    total_orders = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return int(total_orders or 0)

def fetch_average_order_value(days: int | None = None) -> float:
    conn = get_connection()
    cursor = conn.cursor()

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

# AGENT TOOLS (WRAPPERS)

@function_tool
def get_total_revenue() -> float:
    return fetch_total_revenue()

@function_tool
def get_top_customers(limit: int = 3) -> list:
    return fetch_top_customers(limit)

@function_tool
def get_top_products(limit: int = 3) -> list:
    return fetch_top_products(limit)

@function_tool
def get_total_orders() -> int:
    return fetch_total_orders()

@function_tool
def get_average_order_value() -> float:
    return fetch_average_order_value()