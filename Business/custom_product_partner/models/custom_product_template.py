# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CustomProductTemplate(models.Model):
    _inherit = 'product.template'

    company_id = fields.Many2one('res.company', string='Company', index=True,
                                 default=lambda self: self.env.user.company_id)


class CustomPartner(models.Model):
    _inherit = 'res.partner'

    company_id = fields.Many2one('res.company', string='Company', index=True,
                                 default=lambda self: self.env.user.company_id)

    property_account_payable_id = fields.Many2one('account.account', company_dependent=True,
                                                  string="Account Payable",
                                                  domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False), ('company_id', '=', [lambda self: self.env.user.company_id])]",
                                                  help="This account will be used instead of the default one as the payable account for the current partner",
                                                  required=True)
    property_account_receivable_id = fields.Many2one('account.account', company_dependent=True,
                                                     string="Account Receivable",
                                                     domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False), ('company_id', '=', [lambda self: self.env.user.company_id])]",
                                                     help="This account will be used instead of the default one as the receivable account for the current partner",
                                                     required=True)
