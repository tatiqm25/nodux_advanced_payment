# -*- coding: utf-8 -*-
# Copyright (c) 2015, NODUX and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class PaymentAdvanced(Document):
	def generate_advanced(self):
		self.save()
		default_cash_account = frappe.db.get_value("Company", {"company_name": self.company}, "default_cash_account")
		default_receivable_account = frappe.db.get_value("Company", {"company_name": self.company}, "default_receivable_account")
		list_advanced = frappe.db.get_value("List Payment Advanced", {"customer":self.customer}, "inicial")

		if list_advanced:
			new_list_advanced = frappe.get_doc("List Payment Advanced", {"customer":self.customer})
			new_list_advanced.inicial = new_list_advanced.inicial + self.total
			new_list_advanced.append('sale_advanced', self)
			new_list_advanced.save()

		else:
			new_list_advanced = frappe.get_doc({
			    "doctype":"List Payment Advanced",
			    "customer": self.customer,
				"customer_name":self.customer,
				"inicial": self.total,
				"utilizado": 0,
				"balance": 0
			})
			new_list_advanced.append('sale_advanced',self)
			new_list_advanced.save()
			new_list_advanced.docstatus = 1
			new_list_advanced.save()

		lined = frappe.get_doc({
			"doctype": "Journal Entry Account",
			"account": default_cash_account,
			"debit_in_account_currency":self.total,
			"credit_in_account_currency":0,
		})
		linec = frappe.get_doc({
			"doctype": "Journal Entry Account",
			"account": default_receivable_account,
			"debit_in_account_currency":0,
			"credit_in_account_currency":self.total,
			"is_advance": "Yes",
			"party_type": "Customer",
			"party": self.customer,
		})
		journal = frappe.get_doc({
			"doctype":"Journal Entry",
			"voucher_type": "Journal Entry",
			"posting_date": nowdate(),
		})

		journal.append('accounts', lined)
		journal.append('accounts', linec)
		journal.save()
		journal.docstatus = 1
		journal.save()
		self.status = "Done"
		self.docstatus = 1
		self.save()
