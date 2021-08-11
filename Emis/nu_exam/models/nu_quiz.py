# -*- coding: utf-8 -*-
from odoo import api, fields, models


# ------------------------------------
# Exam Session Class
# ------------------------------------
# class ExamSession(models.Model):
#     _name = 'exam.session'
#     _description = 'Exam Session'
#     _rec_name = 'name'
#
#     name = fields.Char('Academic Session', required=True)
#     description = fields.Html('Description')
#
#     student_input_ids = fields.One2many(
#         "student.input",
#         "exam_session_id",
#         string="Student Assignments",
#         help="Enter student assignments",
#     )
#
#     state = fields.Selection(
#         [("draft", "Draft"), ("active", "Active"), ("done", "Done")],
#         "Status",
#         default="draft",
#         help="State of Quiz",
#     )
#
#     def active_exam_session(self):
#         self.state = "active"
#
#     def done_exam_session(self):
#         self.state = "done"
