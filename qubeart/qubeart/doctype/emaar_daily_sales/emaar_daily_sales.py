# Copyright (c) 2025, Vivek and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe import _
from frappe.model.document import Document

class EmaarDailySales(Document):
    pass

def validate(doc, method):
    if not doc.date:
        frappe.throw("Please select a date.")

    # Fetch all submitted Sales Invoices for the selected date
    sales_invoices = frappe.get_all(
        "Sales Invoice",
        filters={
            "custom_branch": "Qube Art General Trading LLC(Branch)",
            "posting_date": doc.date,
            "docstatus": 1
        },
        fields=["net_total"]
    )

    total_amount = sum(invoice["net_total"] for invoice in sales_invoices)
    doc.total_amount = total_amount
    doc.invoice_count = len(sales_invoices)


@frappe.whitelist()
def send_emaar_data(docname):
    doc = frappe.get_doc("Emaar Daily Sales", docname)

    payload = {
        "SalesDataCollection": {
            "SalesInfo": [
                {
                    "UnitNo": "DHM-P1-025",
                    "LeaseCode": "t0019893",
                    "SalesDate": str(doc.date),
                    "TransactionCount": doc.invoice_count,
                    "NetSales": doc.total_amount
                }
            ]
        }
    }

    headers = {
        "Content-Type": "application/json",
        "x-apikey": "EkI9OscNHYU3hO5G92gdfGFXS80g2rEQ"
    }

    try:
        response = requests.post(
            url="https://apidev.emaar.com/etenantsales/dailysales",
            headers=headers,
            json=payload,
            timeout=10
        )

        # Store full raw response text
        doc.api_response = response.text
        doc.save(ignore_permissions=True)
       
        if response.status_code == 200:
            frappe.log_error(title="Emaar Daily Sales Data Send Success Log",message = response.text )
            return "success"
            
        else:
            try:
                error_msg = response.json().get("ErrorMsg", "Unknown error")
            except Exception:
                error_msg = response.text
            frappe.log_error(title="Emaar Daily Sales Data Send Failed Log",message = error_msg )
            # frappe.throw(f"Emaar API Error: {error_msg}")

    except Exception:
        error_text = frappe.get_traceback()
        doc.api_response = error_text
        doc.save(ignore_permissions=True)
        frappe.log_error(error_text, _("Emaar API Exception"))
        # frappe.throw("Failed to connect to Emaar API.")
