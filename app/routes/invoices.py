from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.services.invoices import list_invoices_for_customer, export_invoices_csv
from app.services.notifications import notify_export_ready

router = APIRouter()


@router.get("/customers/{customer_id}/invoices")
def get_invoices(customer_id: int, page: int = 1, page_size: int = 50,
                 user=Depends(get_current_user)):
    return list_invoices_for_customer(customer_id, page, page_size)


@router.get("/customers/{customer_id}/invoices/export")
def export_invoices(customer_id: int, user=Depends(get_current_user)):
    csv_data = export_invoices_csv(customer_id)
    notify_export_ready(user["email"], customer_id)
    return {"csv": csv_data}
