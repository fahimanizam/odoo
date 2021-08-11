
from odoo import models, fields, api, _

class DailySalesStatement(models.TransientModel):
    _name = 'daily.sales.statement'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    user_ids = fields.Many2many('res.users', string="Salesperson", required=True)

    def print_due_report_by_salesperson(self):
        sales_invoice = self.env['account.move'].search([])
        due_groupby_dict = {}
        for salesperson in self.user_ids:
            filtered_sale_invoice = list(filter(lambda x: x.invoice_date != 0 and x.state != 'draft' and x.invoice_user_id == salesperson, sales_invoice))
            filtered_by_date = list(filter(lambda x: x.invoice_date >= self.start_date and x.invoice_date <= self.end_date, filtered_sale_invoice))
            due_groupby_dict[salesperson.name] = filtered_by_date
        final_dist = {}
        for salesperson in due_groupby_dict.keys():
            sale_data = []
            for order in due_groupby_dict[salesperson]:
                temp_data = []
                temp_data.append(order.name)
                temp_data.append(order.invoice_date)
                temp_data.append(order.partner_id.name)
                # temp_data.append(order._get_reconciled_invoices_partials())
                bank_id = 0
                cash_id = 0
                for partial, amount, counterpart_line in order._get_reconciled_invoices_partials():
                    journal_name = counterpart_line.journal_id.name
                    if journal_name == 'Bank':
                        bank = partial.amount
                        bank_id = bank_id + bank
                    elif journal_name == 'Cash':
                        cash = partial.amount
                        cash_id = cash_id + cash
                temp_data.append(cash_id)
                temp_data.append(bank_id)
                temp_data.append(order.amount_total)
                temp_data.append(order.amount_residual_signed)
                sale_data.append(temp_data)
            final_dist[salesperson] = sale_data
        datas = {
            'ids': self,
            'model': 'due.collection.report',
            'form': final_dist,
            'start_date': self.start_date,
            'end_date': self.end_date
        }
        return self.env.ref('daily_sales_statement.action_daily_sales_statement_report').report_action([], data=datas)
