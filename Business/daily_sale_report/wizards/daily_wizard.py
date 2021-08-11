# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime


class DailyWizard(models.TransientModel):
    _name = 'odoo.daily.sales'

    date_today = fields.Date(string="Date Today", required=False)
    categ_id = fields.Many2many(comodel_name="product.category", string="Select Category", required=False,)
    dailylines = fields.One2many(comodel_name="odoo.daily.sales.template", inverse_name="wiz_id", string="Data",
                                 readonly=True)

    def _get_daily_lines(self):

        if self.categ_id:
            domain = tuple(self.categ_id.ids) if len(self.categ_id) > 1 else (self.categ_id.ids[0], 0)
            query = ("""SELECT sale_report.order_id as order_name, sale_order.date_order as odate, sale_report.partner_id as customer_name, sale_report.user_id as sale_person,sale_report.discount_amount as discount_amount,qty_invoiced, sale_report.categ_id as pro_categ, sale_report.product_id as pro_name, sale_report.price_unit as price_unit, sale_report.price_subtotal as price_subtotal,sale_report.product_uom_qty as product_uom_qty
                    FROM sale_report
                    join sale_order on sale_order.id = sale_report.order_id
                    join res_partner on res_partner.id = sale_report.partner_id
                    join res_users on res_users.id = sale_report.user_id
                    join product_product on product_product.id = sale_report.product_id
                    join product_category on product_category.id = sale_report.categ_id
                    where DATE(sale_order.date_order) = \'{date_today}\'  and sale_report.categ_id in {categ_ids}
                    GROUP BY customer_name, sale_person,order_name,pro_categ,pro_name, price_unit,price_subtotal, product_uom_qty, discount_amount,qty_invoiced,sale_order.date_order
                    ORDER BY pro_categ,sale_order.date_order
                                 """.format(date_today=self.date_today, categ_ids=domain))
        else:
            query = ("""SELECT sale_report.order_id as order_name, sale_order.date_order as odate, sale_report.partner_id as customer_name, sale_report.user_id as sale_person,sale_report.discount_amount as discount_amount,qty_invoiced, sale_report.categ_id as pro_categ, sale_report.product_id as pro_name, sale_report.price_unit as price_unit, sale_report.price_subtotal as price_subtotal,sale_report.product_uom_qty as product_uom_qty
                 FROM sale_report
                join sale_order  on sale_order.id = sale_report.order_id
                join res_partner on res_partner.id = sale_report.partner_id
                join res_users on res_users.id = sale_report.user_id
                join product_product on product_product.id = sale_report.product_id
                join product_category on product_category.id = sale_report.categ_id
                where DATE(sale_order.date_order) = \'{date_today}\'
                GROUP BY customer_name, sale_person, order_name, pro_categ, pro_name,price_unit,price_subtotal, product_uom_qty, discount_amount,qty_invoiced,sale_order.date_order
                ORDER BY pro_categ,sale_order.date_order
                             """.format(date_today=self.date_today))

        self._cr.execute(query)
        dailylines = self._cr.dictfetchall()
        return dailylines

    def _today_date(self):
        date_today = self.date_today
        return date_today

    def daily_preview(self):
        self.dailylines = [(5, 0, 0)]
        line_list = []
        dailylines = self._get_daily_lines()

        for line in dailylines:
            line_list.append((0, 0, {
                'categ': self.env['product.category'].search([('id', '=', line.get('pro_categ'))]).name,
                'qty': str(line.get('product_uom_qty')),
                'product_name': self.env['product.product'].search([('id', '=', line.get('pro_name'))]).name,
                'odate': str(line.get('odate')),
            }))
        self.dailylines = line_list
        return {
            'type': 'ir.actions.act_window',
            'res_model': "odoo.daily.sales",
            'res_id': self.id,
            'view_mode': 'form,tree',
            'name': 'Daily Sales',
            'target': 'new'
        }

    def daily_print_pdf(self):
        data2 = {}
        dailylines = self._get_daily_lines()
        date_today = self._today_date()
        data2['dailylines'] = dailylines
        data2['date_today'] = date_today
        print(dailylines)
        print(date_today)
        return self.env.ref('daily_sale_report.daily_pdf_reportid').report_action([], data=data2)



class Template(models.TransientModel):
    _name = 'odoo.daily.sales.template'

    odate = fields.Char(string="Order Date", required=False, )
    categ = fields.Char(string="Category", required=False, )
    qty = fields.Char(string="Qty", required=False, )
    product_name = fields.Char(string="Product", required=False, )

    wiz_id = fields.Many2one(comodel_name="odoo.daily.sales")
