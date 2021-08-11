# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime

class PurchaseWizard(models.TransientModel):
    _name = 'odoo.item.issue'

    date_from = fields.Date(string="Date From", required=False)
    date_to = fields.Date(string="Date To", required=False)
    categ_id = fields.Many2many(comodel_name="product.category", string="Select Category", required=False, )
    itemlines = fields.One2many(comodel_name="item.issue.template", inverse_name="wiz_id", string="Data",
                            readonly=True)

    def _get_item_issue_lines(self):
        if self.categ_id:
            domain = tuple(self.categ_id.ids) if len(self.categ_id) > 1 else (self.categ_id.ids[0], 0)
            query = ("""SELECT sale_report.order_id as order_name, sale_order.date_order as odate, sale_report.partner_id as customer_name, sale_report.user_id as sale_person,sale_report.discount_amount as discount_amount,qty_invoiced, sale_report.categ_id as pro_categ, sale_report.product_id as pro_name,sale_report.price_unit as price_unit, sale_report.price_subtotal as price_subtotal, sale_report.product_uom_qty as product_uom_qty, sale_report.tax as tax, sale_report.name as pro_ref,sale_report.cus_ref as cus_ref,sale_report.product_uom_qty as product_uom_qty
                        FROM sale_report
                        join sale_order on sale_order.id = sale_report.order_id
                        join res_partner on res_partner.id = sale_report.partner_id
                        join res_users on res_users.id = sale_report.user_id
                        join product_product on product_product.id = sale_report.product_id
                        join product_category on product_category.id = sale_report.categ_id
                        where sale_order.date_order  >=\'{date_form}\' and  sale_order.date_order <=\'{date_to}\'   and sale_report.categ_id in {categ_ids}
                        GROUP BY customer_name, sale_person,order_name,pro_categ,pro_name,price_unit,price_subtotal,product_uom_qty, discount_amount,qty_invoiced,sale_order.date_order,tax,pro_ref,cus_ref,product_uom_qty
                        ORDER BY pro_categ,sale_order.date_order
                                     """.format(date_form=self.date_from, date_to=self.date_to, categ_ids=domain))
        else:
            query = ("""SELECT sale_report.order_id as order_name, sale_order.date_order as odate, sale_report.partner_id as customer_name, sale_report.user_id as sale_person,sale_report.discount_amount as discount_amount,qty_invoiced, sale_report.categ_id as pro_categ, sale_report.product_id as pro_name,sale_report.price_unit as price_unit, sale_report.price_subtotal as price_subtotal,sale_report.product_uom_qty as product_uom_qty,sale_report.tax as tax, sale_report.name as pro_ref,sale_report.cus_ref as cus_ref,sale_report.product_uom_qty as product_uom_qty
                     FROM sale_report
                    join sale_order  on sale_order.id = sale_report.order_id
                    join res_partner on res_partner.id = sale_report.partner_id
                    join res_users on res_users.id = sale_report.user_id
                    join product_product on product_product.id = sale_report.product_id
                    join product_category on product_category.id = sale_report.categ_id
                    where sale_order.date_order  >=\'{date_form}\' and  sale_order.date_order <=\'{date_to}\'
                    GROUP BY customer_name, sale_person, order_name, pro_categ, pro_name,price_unit,price_subtotal,product_uom_qty, discount_amount,qty_invoiced,sale_order.date_order,tax,pro_ref,cus_ref,product_uom_qty
                    ORDER BY pro_categ,sale_order.date_order
                                 """.format(date_form=self.date_from, date_to=self.date_to))

        self._cr.execute(query)
        itemlines = self._cr.dictfetchall()
        return itemlines


    def _start_date(self):
        date_form = self.date_from
        return date_form

    def _end_date(self):
        date_to = self.date_to
        return date_to

    def item_issue_preview(self):
        self.itemlines = [(5, 0, 0)]
        line_list = []
        itemlines = self._get_item_issue_lines()

        for line in itemlines:
            line_list.append((0, 0, {
                'categ': self.env['product.category'].search([('id', '=', line.get('pro_categ'))]).name,
                'qty': str(line.get('product_uom_qty')),
                'product_name': self.env['product.product'].search([('id', '=', line.get('pro_name'))]).name,
                'odate': str(line.get('odate')),
            }))
        self.itemlines = line_list
        return {
            'type': 'ir.actions.act_window',
            'res_model': "odoo.item.issue",
            'res_id': self.id,
            'view_mode': 'form,tree',
            'name': 'Item Issue Register',
            'target': 'new'
        }

    def item_issue_print_pdf(self):
        data1 = {}
        itemlines = self._get_item_issue_lines()
        date_form = self._start_date()
        date_to = self._end_date()
        data1['itemlines'] = itemlines
        data1['date_form'] = date_form
        data1['date_to'] = date_to
        return self.env.ref('item_issue_report.item_issue_pdf_reportid').report_action([], data=data1)


class ItemIssueTemplate(models.TransientModel):
    _name = 'item.issue.template'

    odate = fields.Char(string="Order Date", required=False, )
    categ = fields.Char(string="Category", required=False, )
    qty = fields.Char(string="Qty", required=False, )
    product_name = fields.Char(string="Product", required=False, )

    wiz_id = fields.Many2one(comodel_name="odoo.item.issue")