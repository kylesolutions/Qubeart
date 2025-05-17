# Copyright (c) 2025, Vivek and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = [
        {"label": "Invoice", "fieldname": "name", "fieldtype": "Link", "options": "Sales Invoice", "width": 120},
        {"label": "Customer", "fieldname": "customer_name", "fieldtype": "Data", "width": 180},
        {"label": "Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": "Net Total", "fieldname": "net_total", "fieldtype": "Currency", "width": 120},
        {"label": "Tax Amount", "fieldname": "total_taxes_and_charges", "fieldtype": "Currency", "width": 120},
        {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "width": 120},
    ]

    conditions = ""
    if filters.get("from_date"):
        conditions += " AND si.posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND si.posting_date <= %(to_date)s"
    if filters.get("sales_person"):
        conditions += """ AND EXISTS (
            SELECT 1 FROM `tabSales Team` st 
            WHERE st.parent = si.name AND st.sales_person = %(sales_person)s
        )"""

    data = frappe.db.sql(f"""
        SELECT
            si.name, si.customer_name, si.posting_date,
            si.net_total, si.total_taxes_and_charges, si.grand_total
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1 {conditions}
        ORDER BY si.posting_date DESC
    """, filters, as_dict=True)

    return columns, data
