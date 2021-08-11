# -*- coding: utf-8 -*-
# from odoo import http


# class CustomErp1(http.Controller):
#     @http.route('/custom_erp_1/custom_erp_1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_erp_1/custom_erp_1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_erp_1.listing', {
#             'root': '/custom_erp_1/custom_erp_1',
#             'objects': http.request.env['custom_erp_1.custom_erp_1'].search([]),
#         })

#     @http.route('/custom_erp_1/custom_erp_1/objects/<model("custom_erp_1.custom_erp_1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_erp_1.object', {
#             'object': obj
#         })
