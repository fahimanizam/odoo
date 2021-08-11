# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


# Custom Product Template
class CustomDailyAttendance(models.Model):
    _inherit = 'op.attendance.sheet'

    @api.depends('total_present','total_absent')
    def _compute_total(self):
        for record in self:
            record.total_student = record.total_present + record.total_absent

    @api.depends('total_present','total_student')
    def _compute_present_percentage(self):
        for record in self:
            present_p = 0
            if record.total_student > 0 and record.total_present > 0:
                present_p = int((record.total_present / record.total_student) * 100)
            record.total_percentage = str(present_p) + "%"

    total_percentage = fields.Char(compute="_compute_present_percentage",
                                   store=True,
                                   string='Percentage of Present Student',
                                   help="Present Student Percentage")
    total_student = fields.Integer(compute="_compute_total",
                                   store=True,
                                   string='Total Student',
                                   help="Total Student")


class CustomOpAttendanceLine(models.Model):
    _inherit = "op.attendance.line"
    # _order = 'roll_number'
    # _rec_name = 'roll_number'

    roll_number = fields.Char('Roll Number', help='Roll Number')
    student_id = fields.Many2one(
        'op.student', 'Student', required=True, track_visibility="onchange")

    @api.onchange('roll_number','student_id')
    def onchange_roll(self):
        self.roll_number = self.student_id.roll_number