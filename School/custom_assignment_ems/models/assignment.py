# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


# ------------------------------------
# Custom School Student Assignment
# ------------------------------------
class CustomSchoolStudentAssignment(models.Model):
    _inherit = 'school.student.assignment'

    @api.onchange("student_id")
    def onchange_student(self):
        self.stud_roll_no = self.student_id.roll_no
