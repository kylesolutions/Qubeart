// Copyright (c) 2025, Vivek and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Sales Report"] = {
	"filters": [
		 {
    "fieldname": "from_date",
    "label": "From Date",
    "fieldtype": "Date",
    "default": "Today",
    "reqd": 1
  },
  {
    "fieldname": "to_date",
    "label": "To Date",
    "fieldtype": "Date",
    "default": "Today",
    "reqd": 1
  },
  {
    "fieldname": "sales_person",
    "label": "Sales Person",
    "fieldtype": "Link",
    "options": "Sales Person"
  }
	]
};
