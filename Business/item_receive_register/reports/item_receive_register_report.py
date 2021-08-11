#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo import tools
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class CustomItemPurchaseReport(models.Model):
    _inherit = "purchase.report"

    tax = fields.Float('Tax', readonly=True)
    vendor_ref = fields.Char('Vendor Reference', readonly=True)
    pro_ref = fields.Char('Reference', readonly=True)

    def _select(self):
        res = super(CustomItemPurchaseReport, self)._select()
        select_str = res + """, l.price_tax as tax,po.partner_ref as vendor_ref,po.name as pro_ref"""
        return select_str


    def _group_by(self):
        return super(CustomItemPurchaseReport,
                     self)._group_by() + ", l.price_tax,po.partner_ref,po.name"
    # l.taxes_id as taxes_id,
    # l.taxes_id,
    # join account_tax on account_tax.id = purchase_report.taxes_id
    # ,


class ItemIssueReportCard(models.AbstractModel):
    _name = 'report.item_issue_report.item_receive_template_id'

    @api.model
    def _get_report_values(self, docids, data=None):
        itemreceivelines = data.get('itemreceivelines', [])
        docargs = {
            'itemreceivelines': itemreceivelines,
        }
        return docargs
