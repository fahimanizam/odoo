from odoo import api, models


class DailySalesStateReport(models.AbstractModel):
    _name = 'report.daily_sales_statement.daily_sales_statement_template_id'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['form'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
        }