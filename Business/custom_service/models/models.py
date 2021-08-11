# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProductProduct(models.Model):
    _inherit = 'product.template'

    is_a_parts = fields.Boolean(
        'Is a Computer Part', default=False,
        help="Specify if the product is a computer part or not.")


class CustomBrandModel(models.Model):
    _inherit = 'brand.model'

    mobile_brand_name = fields.Many2one('mobile.brand', string="Brand", required=True)

class CustomMobileBrand(models.Model):
    _inherit = 'mobile.brand'

    brand_name = fields.Char(string="Brand", required=True)


class CustomMobileService(models.Model):
    _inherit = 'mobile.service'

    imei_no = fields.Char(string="Mac Address")

    brand_name = fields.Many2one('mobile.brand', string="Brand")

    request_id = fields.Many2one(
        'request.request', string='Request', required=True,
        readonly=False)

    # def _get_request_summary(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'request_id': self.active_id
    #     }


class CustomRequest(models.Model):
    _inherit = 'request.request'

    service_count = fields.Integer(
        'Service', compute='_compute_service',
        help='Number of service created by user')

    def _compute_service(self):
        self.service_count = 0
        for service in self:
            service.service_count = self.env['mobile.service'].search_count(
                [('request_id', '=', service.id)])
