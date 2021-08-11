# -*- coding: utf-8 -*-
from pytz import timezone
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CustomResPartner(models.Model):
    _inherit = 'res.partner'


    # def custom_action_customer(self):
    #     self.ensure_one()
    #     action = self.env["ir.actions.actions"]._for_xml_id("account.res_partner_action_customer")
    #     action['domain'] = [('customer', '=', True)]
    #     action['context'] = dict(self._context, default_company_id=self.user.company_id)
    #     return action

    # company_id = fields.Many2one('res.company', string='Company', index=True,
    #                              default=lambda self: self.env.user.company_id)
