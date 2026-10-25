import csv
import io
from app.db import get_connection

TAX_RATE = 0.18


def invoice_total(items):
    subtotal = sum(i["quantity"] * i["unit_price"] for i in items)
    return round(subtotal * (1 + TAX_RATE), 2)


def list_invoices_for_customer(customer_id, page, page_size):
    conn = get_connection()
    offset = (page - 1) * page_size
    rows = conn.execute(
        "SELECT id, status, created_at FROM invoices "
        "WHERE customer_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (customer_id, page_size, offset),
    ).fetchall()

    invoices = []
    for row in rows:
        items = conn.execute(
            "SELECT description, quantity, unit_price FROM invoice_items "
            "WHERE invoice_id = ?",
            (row[0],),
        ).fetchall()
        items = [{"description": d, "quantity": q, "unit_price": p} for d, q, p in items]
        invoices.append({
            "id": row[0],
            "status": row[1],
            "created_at": row[2],
            "total": invoice_total(items),
        })
    return invoices


def export_invoices_csv(customer_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, status, created_at FROM invoices WHERE customer_id = ?",
        (customer_id,),
    ).fetchall()

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "status", "created_at"])
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()
