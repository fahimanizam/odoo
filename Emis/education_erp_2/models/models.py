# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


#
class CustomStudent(models.Model):
    _inherit = 'crm.lead'

    partner_id = fields.Many2one(
        'res.partner', string='Student', index=True, tracking=10,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")

    partner_name = fields.Char(
        'Institute Name', tracking=20, index=True,
        compute='_compute_partner_id_values', readonly=False, store=True,
        help='The name of the future partner company that will be created while converting the lead into opportunity')
#
#     board_roll_number = fields.Char('Board Roll Number')
#     roll_number = fields.Char('Roll Number')
#     registration_number = fields.Char('Registration Number')
#     active = fields.Boolean(default=True)
#
# class CustomFaculty(models.Model):
#     _inherit = 'op.faculty'
#
#     department = fields.Many2one('op.department', 'Academic Department')

# class CustomStudentMigrate(models.Model):
#     _inherit = "student.migrate"
#
#     department_from_id = fields.Many2one('op.department', 'From Department')
#     department_to_id = fields.Many2one('op.department', 'To Department')

class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id = fields.Many2one(
        'res.partner', string='Student', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )


# class CustomSaleAdvancePaymentInv(models.Model):
#     _inherit = 'sale.advance.payment.inv'
#     deposit_taxes_id = fields.Many2many("account.tax",  string="Student taxes", help="Taxes used for deposits",
#                                         default=_default_deposit_taxes_id)


class InheritedAccountMove(models.Model):
    _inherit = "account.move"

    move_type = fields.Selection(selection=[
        ('entry', 'Journal Entry'),
        ('out_invoice', 'Student Invoice'),
        ('out_refund', 'Student Credit Note'),
        ('in_invoice', 'Vendor Bill'),
        ('in_refund', 'Vendor Credit Note'),
        ('out_receipt', 'Sales Receipt'),
        ('in_receipt', 'Purchase Receipt'),
    ], string='Type', required=True, store=True, index=True, readonly=True, tracking=True,
        default="entry", change_default=True)


