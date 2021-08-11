# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


# ------------------------------------
# Custom Additional Exam Class
# ------------------------------------
class CustomAdditionalExamResult(models.Model):
    _inherit = "additional.exam.result"

    @api.onchange("standard_id")
    def onchange_standard(self):
        if self.standard_id:
            self.a_exam_id = False
            self.student_id = False

    @api.onchange("a_exam_id")
    def onchange_standard(self):
        if self.a_exam_id:
            self.subject_id = self.a_exam_id.subject_id or False

    standard_id = fields.Many2one(
        "school.standard", "Standard", readonly=False, help="School Standard"
    )

    subject_id = fields.Many2one("subject.subject", "Subject Name")

    additional_exam_result = fields.Many2one("all.additional.exam.result", "All Additional Exam", index=True,
                                             ondelete='cascade')

    def _update_student_vals(self, vals):
        student_rec = self.env["student.student"].browse(
            vals.get("student_id")
        )
        vals.update(
            {
                "roll_no_id": student_rec.roll_no,
                "standard_id": student_rec.standard_id.id,
            }
        )


# ------------------------------------
# Custom Additional Exam Class
# ------------------------------------
class AllAdditionalExamResult(models.Model):
    _name = "all.additional.exam.result"

    @api.onchange("student_id")
    def onchange_standard(self):
        if self.student_id:
            self.roll_no = self.student_id.roll_no or False

    standard_id = fields.Many2one(
        "school.standard", "Standard", readonly=False, help="School Standard"
    )

    student_id = fields.Many2one(
        "student.student", "Student Name", required=True, help="Select Student"
    )

    roll_no = fields.Integer(
        "Roll No", help="Student rol no."
    )

    additional_exam_result = fields.One2many("additional.exam.result",
                                             string="additional exam result", compute='_compute_exam',
                                             help='Total Additional exam')

    @api.depends('standard_id', 'student_id')
    def _compute_exam(self):
        student_obj = self.env['additional.exam.result']
        for rec in self:
            rec.additional_exam_result = student_obj. \
                search([('standard_id', '=', rec.standard_id.id),
                        ('student_id', '=', rec.student_id.id),
                        ('active', '=', True)])
