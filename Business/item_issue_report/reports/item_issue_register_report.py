#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo import tools
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class CustomItemIssueReport(models.Model):
    _inherit = "sale.report"

    tax = fields.Float('Tax', readonly=True)
    cus_ref = fields.Char('Customer Reference', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['tax'] = ', l.price_tax as tax'
        fields['cus_ref'] = ', s.client_order_ref as cus_ref'

        groupby += """, l.price_tax,s.client_order_ref
                """
        return super(CustomItemIssueReport, self)._query(with_clause, fields, groupby, from_clause)


class ItemIssueReportCard(models.AbstractModel):
    _name = 'report.item_issue_report.item_issue_template_id'

    @api.model
    def _get_report_values(self, docids, data=None):
        itemlines = data.get('itemlines', [])
        docargs = {
            'itemlines': itemlines,
        }
        return docargs
