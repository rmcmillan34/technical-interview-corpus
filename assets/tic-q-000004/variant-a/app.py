from fastapi import FastAPI

app = FastAPI()

@app.get("/api/invoices/{invoice_id}")
def get_invoice(invoice_id: int):
    # Authentication is handled by middleware.
    return db.get_invoice(invoice_id)
