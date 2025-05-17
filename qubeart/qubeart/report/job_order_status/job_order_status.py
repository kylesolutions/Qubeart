# Copyright (c) 2025, Vivek and contributors
# For license information, please see license.txt



# import frappe

import frappe

def execute(filters=None):
    columns = [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 150},
        {"label": "Qube Job Order ID", "fieldname": "name", "fieldtype": "Link", "options": "Qube Job Order", "width": 150},
        {"label": "Sales Order", "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 130},
        {"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data", "width": 150},
        {"label": "Job Order No", "fieldname": "customers_purchase_order", "fieldtype": "Data", "width": 150},
        {"label": "Sales Person", "fieldname": "sales_person", "fieldtype": "Data", "width": 150},
        {"label": "QC Status", "fieldname": "qc_status", "fieldtype": "Data", "width": 120},
        {"label": "Production Status", "fieldname": "production_status", "fieldtype": "Data", "width": 150},
    ]

    conditions = "1=1"
    if filters.get("qc_status"):
        conditions += " AND qjo.qc_status = %(qc_status)s"
    if filters.get("production_status"):
        conditions += " AND qjo.production_status = %(production_status)s"
    if filters.get("from_date"):
        conditions += " AND qjo.creation >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND qjo.creation <= %(to_date)s"

    data = frappe.db.sql(f"""
        SELECT
            qjo.date,
            qjo.name,
            qjo.customers_purchase_order,
            qjo.sales_order,
            qjo.customer_name,
            st.sales_person,
            qjo.qc_status,
            qjo.production_status
        FROM `tabQube Job Order` qjo
        LEFT JOIN `tabSales Team` st ON st.parent = qjo.sales_order AND st.parenttype = 'Sales Order'
        WHERE {conditions}
        ORDER BY qjo.modified DESC
    """, filters, as_dict=True)

    return columns, data
