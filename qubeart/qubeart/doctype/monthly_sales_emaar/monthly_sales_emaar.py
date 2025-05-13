# Copyright (c) 2025, Vivek and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe import _
from frappe.model.document import Document


class MonthlySalesEmaar(Document):
	pass


def validate(doc, method):
    if not doc.from_date or not doc.to_date:
        frappe.throw("Please select both From Date and To Date.")

    if doc.from_date > doc.to_date:
        frappe.throw("From Date cannot be greater than To Date.")

    # Fetch all submitted Sales Invoices between from_date and to_date
    sales_invoices = frappe.get_all(
        "Sales Invoice",
        filters={
            "custom_branch": "Qube Art General Trading LLC(Branch)",
            "posting_date": ["between", [doc.from_date, doc.to_date]],
            "docstatus": 1
        },
        fields=["net_total"]
    )

    # Calculate total net amount and invoice count
    total_amount = sum(invoice["net_total"] for invoice in sales_invoices)
    doc.total_amount = total_amount
    doc.invoice_count = len(sales_invoices)

@frappe.whitelist()
def send_emaar_data(docname):
    doc = frappe.get_doc("Monthly Sales Emaar", docname)

    payload = {
        "SalesDataCollection": {
            "SalesInfo": [
                {
                    "UnitNo": "DHM-P1-025",
                    "LeaseCode": "t0019893",
                    "SalesDateFrom": str(doc.from_date),
        			"SalesDateTo": str(doc.to_date),
                    "TransactionCount": doc.invoice_count,
                    "TotalSales": doc.total_amount,
					"Remarks": "Remarks"
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
            url="https://apidev.emaar.com/etenantsales/casualsales",
            headers=headers,
            json=payload,
            timeout=10
        )

        # Store full raw response text
        doc.api_response = response.text
        doc.save(ignore_permissions=True)

        if response.status_code == 200:
            return "success"
        else:
            try:
                error_msg = response.json().get("ErrorMsg", "Unknown error")
            except Exception:
                error_msg = response.text

            frappe.throw(f"Emaar API Error: {error_msg}")

    except Exception:
        error_text = frappe.get_traceback()
        doc.api_response = error_text
        doc.save(ignore_permissions=True)
        frappe.log_error(error_text, _("Emaar API Exception"))
        frappe.throw("Failed to connect to Emaar API.")
