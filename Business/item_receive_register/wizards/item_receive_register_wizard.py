# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime

class PurchaseWizard(models.TransientModel):
    _name = 'item.receive.register'

    date_from = fields.Date(string="Date From", required=False)
    date_to = fields.Date(string="Date To", required=False)
    categ_id = fields.Many2many(comodel_name="product.category", string="Select Category", required=False, )
    itemreceivelines = fields.One2many(comodel_name="item.receive.template", inverse_name="wiz_id", string="Data",
                            readonly=True)

    def _get_item_receive_lines(self):

        if self.categ_id:
            domain = tuple(self.categ_id.ids) if len(self.categ_id) > 1 else (self.categ_id.ids[0], 0)
            query = ("""SELECT purchase_report.order_id as order_name, purchase_order.date_order as odate, purchase_report.partner_id as customer_name, purchase_report.user_id as purchase_person,purchase_report.qty_invoiced as qty_invoiced, purchase_report.category_id as pro_categ, purchase_report.product_id as pro_name, purchase_report.price_unit as price_unit, purchase_report.price_subtotal as price_subtotal,purchase_report.product_qty as product_qty, purchase_report.pro_ref as pro_ref,purchase_report.vendor_ref as vendor_ref,purchase_report.tax as tax
                    FROM purchase_report
                    join purchase_order on purchase_order.id = purchase_report.order_id
                    join res_partner on res_partner.id = purchase_report.partner_id
                    join res_users on res_users.id = purchase_report.user_id
                    join product_product on product_product.id = purchase_report.product_id
                    join product_category on product_category.id = purchase_report.category_id
                    where purchase_order.date_order  >=\'{date_form}\' and  purchase_order.date_order <=\'{date_to}\' and purchase_report.category_id in {categ_ids}
                    GROUP BY customer_name, purchase_person,order_name,pro_categ,pro_name, price_unit,price_subtotal, product_qty, qty_invoiced,purchase_order.date_order,pro_ref,vendor_ref,tax
                    ORDER BY pro_categ,purchase_order.date_order
                                 """.format(date_form=self.date_from, date_to=self.date_to, categ_ids=domain))
        else:
            query = ("""SELECT purchase_report.order_id as order_name, purchase_order.date_order as odate, purchase_report.partner_id as customer_name, purchase_report.user_id as purchase_person,purchase_report.qty_invoiced as qty_invoiced, purchase_report.category_id as pro_categ, purchase_report.product_id as pro_name, purchase_report.price_unit as price_unit, purchase_report.price_subtotal as price_subtotal,purchase_report.product_qty as product_qty,purchase_report.pro_ref as pro_ref,purchase_report.vendor_ref as vendor_ref,purchase_report.tax as tax
                 FROM purchase_report
                join purchase_order  on purchase_order.id = purchase_report.order_id
                join res_partner on res_partner.id = purchase_report.partner_id
                join res_users on res_users.id = purchase_report.user_id
                join product_product on product_product.id = purchase_report.product_id
                join product_category on product_category.id = purchase_report.category_id
                where purchase_order.date_order  >=\'{date_form}\' and  purchase_order.date_order <=\'{date_to}\'
                GROUP BY customer_name, purchase_person, order_name, pro_categ, pro_name,price_unit,price_subtotal, product_qty,qty_invoiced,purchase_order.date_order, pro_ref,vendor_ref,tax
                ORDER BY pro_categ,purchase_order.date_order
                             """.format(date_form=self.date_from, date_to=self.date_to))

        self._cr.execute(query)
        itemreceivelines = self._cr.dictfetchall()
        return itemreceivelines

    def _start_date(self):
        date_form = self.date_from
        return date_form

    def _end_date(self):
        date_to = self.date_to
        return date_to

    def item_receive_preview(self):
        self.itemreceivelines = [(5, 0, 0)]
        line_list = []
        itemreceivelines = self._get_item_receive_lines()

        for line in itemreceivelines:
            line_list.append((0, 0, {
                'categ': self.env['product.category'].search([('id', '=', line.get('pro_categ'))]).name,
                'qty': str(line.get('qty_invoiced')),
                'product_name': self.env['product.product'].search([('id', '=', line.get('pro_name'))]).name,
                'odate': str(line.get('odate')),
            }))
        self.itemreceivelines = line_list
        return {
            'type': 'ir.actions.act_window',
            'res_model': "odoo.item.issue",
            'res_id': self.id,
            'view_mode': 'form,tree',
            'name': 'Item Receive Register',
            'target': 'new'
        }

    def item_receive_print_pdf(self):
        data1 = {}
        itemreceivelines = self._get_item_receive_lines()
        date_form = self._start_date()
        date_to = self._end_date()
        data1['itemreceivelines'] = itemreceivelines
        data1['date_form'] = date_form
        data1['date_to'] = date_to
        return self.env.ref('item_receive_register.item_receive_pdf_reportid').report_action([], data=data1)


class ItemReceiveTemplate(models.TransientModel):
    _name = 'item.receive.template'

    odate = fields.Char(string="Order Date", required=False, )
    categ = fields.Char(string="Category", required=False, )
    qty = fields.Char(string="Qty", required=False, )
    product_name = fields.Char(string="Product", required=False, )

    wiz_id = fields.Many2one(comodel_name="item.receive.register")