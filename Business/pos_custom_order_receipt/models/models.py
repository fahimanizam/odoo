# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


# Custom Product Template
class ProductTemplate(models.Model):
    _inherit = "product.template"

    warranty = fields.Boolean('Has warranty of  ', default=False)
    year_type = fields.Selection(string='Company Type',
                                 selection=[('1 year', '1 Year'), ('2 year', '2 Year'), ('3 year', '3 Year')])
