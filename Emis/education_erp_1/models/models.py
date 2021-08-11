# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CustomStudent(models.Model):
    _inherit = 'op.student'

    board_roll_number = fields.Char('Board Roll Number')
    roll_number = fields.Char('Roll Number')
    registration_number = fields.Char('Registration Number')
    active = fields.Boolean(default=True)

class CustomFaculty(models.Model):
    _inherit = 'op.faculty'

    faculty = fields.Many2one('edu.faculty', 'Faculty Name', required=True)
    department_id = fields.Many2one(
            'op.department', 'Department',
            default=lambda self:
            self.env.user.dept_id and self.env.user.dept_id.id or False)
    # department = fields.Many2one('op.department', 'Academic Department')

class CustomSubject(models.Model):
    _inherit = 'op.subject'

    faculty_id = fields.Many2one('edu.faculty', 'Faculty', required=True)
    # department_id = fields.Many2one('op.department', 'Department')



    # subject_ids = fields.Many2many('op.subject', string='Subject(s)')

    # @api.onchange('subject_ids')
    # def subject_onchange(self):
    #     return {'domain': {'subject_ids': [('department_id', '=', self.department_id)]}}

    # @api.depends('department_id')
    # def _compute_subject(self):
    #     subject_obj = self.env['op.subject']
    #     for rec in self:
    #         rec.subject_ids = subject_obj. \
    #             search([('department_id', '=', rec.department_id)])


    # @api.onchange("department_id")
    # def onchange_subject_course(self):
    #     self.department_id = self.subject_ids.department_id


# class CustomStudentMigrate(models.Model):
#     _inherit = "student.migrate"
#
#     department_from_id = fields.Many2one('op.department', 'From Department')
#     department_to_id = fields.Many2one('op.department', 'To Department')


