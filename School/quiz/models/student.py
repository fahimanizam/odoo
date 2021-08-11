# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SchoolStudent(models.Model):
    _inherit = 'student.student'

    certifications_count = fields.Integer('Certifications Count', compute='_compute_certifications_count')
    certifications_company_count = fields.Integer('Company Certifications Count', compute='_compute_certifications_company_count')

    @api.depends('is_company')
    def _compute_certifications_count(self):
        read_group_res = self.env['survey.user_input'].sudo().read_group(
            [('student_id', 'in', self.ids), ('scoring_success', '=', True)],
            ['student_id'], 'student_id'
        )
        data = dict((res['student_id'][0], res['student_id_count']) for res in read_group_res)
        for student in self:
            student.certifications_count = data.get(student.id, 0)

    @api.depends('is_company', 'child_ids.certifications_count')
    def _compute_certifications_company_count(self):
        self.certifications_company_count = sum(child.certifications_count for child in self.child_ids)

    def action_view_certifications(self):
        action = self.env["ir.actions.actions"]._for_xml_id("survey.res_partner_action_certifications")
        action['view_mode'] = 'tree'
        action['domain'] = ['|', ('student_id', 'in', self.ids), ('student_id', 'in', self.child_ids.ids)]

        return action
