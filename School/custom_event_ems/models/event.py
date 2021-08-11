# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

# ------------------------------------
# Custom School Event
# ------------------------------------
# class CustomSchoolEvent(models.Model):
#     _inherit = 'school.event'
#
#     @api.onchange("student_id")
#     def onchange_student(self):
#         self.stud_roll_no = self.student_id.roll_no
