from odoo import tools
from odoo import models, fields

class CustomSaleReport(models.Model):
    _inherit = "sale.report"

    price_unit = fields.Float('Total', readonly=True)


    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['price_unit'] = ', l.price_unit as price_unit'

        groupby += """, l.price_unit
            """
        return super(CustomSaleReport, self)._query(with_clause, fields, groupby, from_clause)