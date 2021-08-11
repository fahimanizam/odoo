# -*- coding: utf-8 -*-
from odoo import api, fields, models


# ------------------------------------------------
# Custom Crm & admission inherited Class
# ------------------------------------------------
class CustomCrmLead(models.Model):
    _inherit = 'crm.lead'

    admission_count = fields.Integer(
        'Admission', compute='_compute_admission',
        help='Number of admission created by user')

    def _compute_admission(self):
        self.admission_count = 0
        for admission in self:
            admission.admission_count = self.env['op.admission'].search_count(
                [('strm_id', '=', admission.id)])

    def action_new_op_admission(self):
        action = self.env["ir.actions.actions"]._for_xml_id("custom_strm_emis.action_op_admission_form")
        return action


class OpAdmission(models.Model):
    _inherit = 'op.admission'

    strm_id = fields.Many2one(
        'crm.lead', string='STRM No',
        readonly=False)
