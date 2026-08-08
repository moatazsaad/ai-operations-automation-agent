# Exposes procurement data as plain REST endpoints for the frontend, which
# can't talk to Postgres directly. No query logic lives here - every route
# just calls the existing service function and returns its result.
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.procurement_metrics_service import (
    fetch_low_stock_items,
    fetch_delayed_purchase_orders,
    fetch_supplier_performance,
    fetch_procurement_spend_by_supplier,
    fetch_reorder_recommendations,
    fetch_top_delayed_suppliers,
)

# Every route below is served under /api/metrics/...
router = APIRouter(prefix="/api/metrics", tags=["metrics"])


# --- Response models -------------------------------------------------------
# Each model mirrors the exact dict shape the matching service function
# returns. FastAPI uses these to validate the response and to generate the
# interactive docs at /docs.

class LowStockItem(BaseModel):
    item_name: str
    category: str
    current_stock: int
    reorder_point: int


class DelayedPurchaseOrder(BaseModel):
    purchase_order_id: int
    supplier_name: str
    item_name: str
    expected_delivery_date: str
    status: str


class SupplierPerformance(BaseModel):
    supplier_name: str
    total_purchase_orders: int
    delayed_purchase_orders: int
    delivered_purchase_orders: int
    on_time_deliveries: int
    total_spend: float
    on_time_delivery_rate: float


class SupplierSpend(BaseModel):
    supplier_name: str
    total_spend: float


class ReorderRecommendation(BaseModel):
    item_name: str
    category: str
    current_stock: int
    reorder_point: int
    safety_stock: int
    recommended_order_quantity: int


class TopDelayedSupplier(BaseModel):
    supplier_name: str
    delayed_po_count: int
    average_days_delayed: float
    max_days_delayed: int


# --- Routes -----------------------------------------------------------------
# These are plain "def", not "async def". The service functions underneath
# make blocking psycopg2 calls with no connection pooling - if these routes
# were declared async, a slow query would freeze FastAPI's single event loop,
# which also serves the Slack webhook and the AI agent runner. Plain "def"
# routes run in FastAPI's threadpool instead, so a slow DB call here can't
# block anything else.

@router.get("/low-stock-items", response_model=list[LowStockItem])
def get_low_stock_items():
    return fetch_low_stock_items()


@router.get("/delayed-purchase-orders", response_model=list[DelayedPurchaseOrder])
def get_delayed_purchase_orders():
    return fetch_delayed_purchase_orders()


@router.get("/supplier-performance", response_model=list[SupplierPerformance])
def get_supplier_performance():
    return fetch_supplier_performance()


@router.get("/spend-by-supplier", response_model=list[SupplierSpend])
def get_spend_by_supplier():
    return fetch_procurement_spend_by_supplier()


@router.get("/reorder-recommendations", response_model=list[ReorderRecommendation])
def get_reorder_recommendations():
    return fetch_reorder_recommendations()


@router.get("/top-delayed-suppliers", response_model=list[TopDelayedSupplier])
def get_top_delayed_suppliers(limit: int = 5):
    return fetch_top_delayed_suppliers(limit=limit)
