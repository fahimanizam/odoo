# -*- coding: utf-8 -*-
import base64
from datetime import date
from odoo import api, fields, models
from odoo.modules import get_module_resource


# ---------------------------------------------
# Student Input Class For Answer Submission
# ---------------------------------------------
class StudentInput(models.Model):
    _name = 'student.input'

    # --------------
    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img',
                                         'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())
    # --------------
    name = fields.Char('Student Name')
    nu_roll_no = fields.Char('Nu Roll No')
    nu_reg_no = fields.Char('Nu Registration No')
    # --------------
    department_name = fields.Char('Department Name')
    college_name = fields.Char('College Name')
    semester_name = fields.Char('Semester')
    course_name = fields.Char('Course Name')
    course_code = fields.Char('Course Code')
    # --------------
    submit_date = fields.Datetime(default=date.today())
    # --------------
    exam_session_id = fields.Many2one(
        "exam.session",
        string="Academic Session",
        help="Student Exam Session",
    )
    # --------------
    attachment = fields.Binary(
        "Attach Your file", help="Attached answer"
    )
    # --------------
    student_image = fields.Binary('Student Image', default=_default_image)
    admit_card = fields.Binary('Admit Card', default=_default_image)
    # --------------
    state = fields.Selection(
        [("draft", "Draft"), ("active", "Active"), ("done", "Done")],
        "Status",
        default="draft",
        help="State of Submission",
    )

    # --------------
    def active_submit(self):
        ir_attachment_obj = self.env["ir.attachment"]
        for rec in self:
            attach = {
                "name": "test",
                "datas": rec.attachment,
            }
            ir_attachment_obj.create(attach)
            rec.state = "active"

    # --------------
    def done_submit(self):
        self.state = "done"

