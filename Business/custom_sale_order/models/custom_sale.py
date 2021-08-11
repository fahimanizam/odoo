# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.addons.sale.models.sale import SaleOrder as OriginalSaleOrder


def _prepare_confirmation_values(self):
    return {
        'state': 'sale'
    }


OriginalSaleOrder._prepare_confirmation_values = _prepare_confirmation_values


class CustomSale(models.Model):
    _inherit = 'sale.order'

    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,
                                 help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")

    create_date = fields.Datetime(string='Creation Date', readonly=True,
                                  help="Date on which sales order is created.")

    # @api.onchange('date_order','create_date')
    # def onchange_date(self):
    #     self.date_order = self.create_date
