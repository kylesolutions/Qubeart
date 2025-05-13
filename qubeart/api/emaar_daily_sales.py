import frappe
from frappe.utils import nowdate, add_days
from qubeart.qubeart.doctype.emaar_daily_sales.emaar_daily_sales import send_emaar_data


def create_emaar_daily_sales():
    today = nowdate()
    if not frappe.db.exists("Emaar Daily Sales", {"date": today}):
        doc = frappe.new_doc("Emaar Daily Sales")
        doc.date = today
        doc.insert()
        doc.submit()


# orbit/frappe-bench/apps/qubeart/qubeart/qubeart/doctype/emaar_daily_sales/emaar_daily_sales.py