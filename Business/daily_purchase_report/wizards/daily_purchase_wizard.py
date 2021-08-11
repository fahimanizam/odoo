# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime

class DailyPurchaseWizard(models.TransientModel):
    _name = 'daily.purchase'

    date_today = fields.Date(string="Date Today", required=False)
    categ_id = fields.Many2many(comodel_name="product.category", string="Select Category", required=False, )
    purchaselines = fields.One2many(comodel_name="daily.purchase.template", inverse_name="wiz_id", string="Data",
                            readonly=True)

    def _get_purchase_lines(self):

        if self.categ_id:
            domain = tuple(self.categ_id.ids) if len(self.categ_id) > 1 else (self.categ_id.ids[0], 0)
            query = ("""SELECT purchase_report.order_id as order_name, purchase_order.date_order as odate, purchase_report.partner_id as customer_name, purchase_report.user_id as sale_person,purchase_report.qty_invoiced as qty_invoiced, purchase_report.category_id as pro_categ, purchase_report.product_id as pro_name, purchase_report.price_unit as price_unit, purchase_report.price_subtotal as price_subtotal,purchase_report.product_qty as product_qty
                    FROM purchase_report
                    join purchase_order on purchase_order.id = purchase_report.order_id
                    join res_partner on res_partner.id = purchase_report.partner_id
                    join res_users on res_users.id = purchase_report.user_id
                    join product_product on product_product.id = purchase_report.product_id
                    join product_category on product_category.id = purchase_report.category_id
                    where DATE(purchase_order.date_order) = \'{date_today}\'  and purchase_report.category_id in {categ_ids}
                    GROUP BY customer_name, sale_person,order_name,pro_categ,pro_name, price_unit,price_subtotal, product_qty, qty_invoiced,purchase_order.date_order
                    ORDER BY pro_categ,purchase_order.date_order
                                 """.format(date_today=self.date_today, categ_ids=domain))
        else:
            query = ("""SELECT purchase_report.order_id as order_name, purchase_order.date_order as odate, purchase_report.partner_id as customer_name, purchase_report.user_id as sale_person,purchase_report.qty_invoiced as qty_invoiced, purchase_report.category_id as pro_categ, purchase_report.product_id as pro_name, purchase_report.price_unit as price_unit, purchase_report.price_subtotal as price_subtotal,purchase_report.product_qty as product_qty
                 FROM purchase_report
                join purchase_order  on purchase_order.id = purchase_report.order_id
                join res_partner on res_partner.id = purchase_report.partner_id
                join res_users on res_users.id = purchase_report.user_id
                join product_product on product_product.id = purchase_report.product_id
                join product_category on product_category.id = purchase_report.category_id
                where DATE(purchase_order.date_order) = \'{date_today}\'
                GROUP BY customer_name, sale_person, order_name, pro_categ, pro_name,price_unit,price_subtotal, product_qty,qty_invoiced,purchase_order.date_order
                ORDER BY pro_categ,purchase_order.date_order
                             """.format(date_today=self.date_today))

        self._cr.execute(query)
        purchaselines = self._cr.dictfetchall()
        return purchaselines

    def _today_date(self):
        date_today = self.date_today
        return date_today

    def daily_purchase_preview(self):
        self.purchaselines = [(5, 0, 0)]
        line_list = []
        purchaselines = self._get_purchase_lines()

        for line in purchaselines:
            line_list.append((0, 0, {
                'categ': self.env['product.category'].search([('id', '=', line.get('pro_categ'))]).name,
                'qty': str(line.get('product_qty')),
                'product_name': self.env['product.product'].search([('id', '=', line.get('pro_name'))]).name,
                'odate': str(line.get('odate')),
            }))
        self.purchaselines = line_list
        return {
            'type': 'ir.actions.act_window',
            'res_model': "daily.purchase",
            'res_id': self.id,
            'view_mode': 'form,tree',
            'name': 'Purchase Report',
            'target': 'new'
        }


    def daily_purchase_print_pdf(self):
        data = {}
        purchaselines = self._get_purchase_lines()
        date_today = self._today_date()
        data['purchaselines'] = purchaselines
        data['date_today'] = date_today
        return self.env.ref('daily_purchase_report.daily_purchase_pdf_reportid').report_action([], data=data)


class DailyPurchaseTemplate(models.TransientModel):
    _name = 'daily.purchase.template'

    odate = fields.Char(string="Order Date", required=False, )
    categ = fields.Char(string="Category", required=False, )
    qty = fields.Char(string="Qty", required=False, )
    product_name = fields.Char(string="Product", required=False, )

    wiz_id = fields.Many2one(comodel_name="daily.purchase")