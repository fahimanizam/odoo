#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo import tools
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class CustomPurchaseReport(models.Model):
    _inherit = "purchase.report"

    price_unit = fields.Float('Total', readonly=True)
    qty_invoiced = fields.Float('Qty Invoiced', readonly=True)
    price_subtotal = fields.Float('Untaxed Total', readonly=True)
    product_qty = fields.Float('Qty Ordered', readonly=True)


    def _select(self):
        res = super(CustomPurchaseReport, self)._select()
        select_str = res + """,l.price_unit
         as price_unit, 
         l.qty_invoiced as qty_invoiced, 
         l.price_subtotal as price_subtotal, 
         l.product_qty as product_qty"""
        return select_str

    def _group_by(self):
        return super(CustomPurchaseReport,
                     self)._group_by() + ", l.qty_invoiced, l.price_subtotal, l.product_qty"


class DailyPurchaseReportCard(models.AbstractModel):
    _name = 'report.daily_purchase_report.template_id'

    @api.model
    def _get_report_values(self, docids, data=None):
        purchaselines = data.get('purchaselines', [])
        docargs = {
            'purchaselines': purchaselines,
        }
        return docargs