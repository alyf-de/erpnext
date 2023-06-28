# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_months, flt


class MonthlyDistribution(Document):
	@frappe.whitelist()
	def get_months(self):
		month_list = [
			"January",
			"February",
			"March",
			"April",
			"May",
			"June",
			"July",
			"August",
			"September",
			"October",
			"November",
			"December",
		]
		for idx, m in enumerate(month_list, start=1):
			mnth = self.append("percentages")
			mnth.month = m
			mnth.percentage_allocation = 100.0 / 12
			mnth.idx = idx

	def validate(self):
		total = sum(flt(d.percentage_allocation) for d in self.get("percentages"))

		if flt(total, 2) != 100.0:
			frappe.throw(
				_("Percentage Allocation should be equal to 100%") + " ({0}%)".format(str(flt(total, 2)))
			)


def get_periodwise_distribution_data(distribution_id, period_list, periodicity):
	doc = frappe.get_doc("Monthly Distribution", distribution_id)

	months_to_add = {"Yearly": 12, "Half-Yearly": 6, "Quarterly": 3, "Monthly": 1}[periodicity]

	return {
		d.key: get_percentage(doc, d.from_date, months_to_add)
		for d in period_list
	}


def get_percentage(doc, start_date, period):
	months = [start_date.strftime("%B").title()]

	months.extend(
		add_months(start_date, r).strftime("%B").title() for r in range(1, period)
	)
	return sum(
		d.percentage_allocation for d in doc.percentages if d.month in months
	)
