# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


# ------------------------------------
# Custom Student class
# ------------------------------------
class CustomStudentTemplate(models.Model):
    _inherit = 'student.student'

    roll_no = fields.Integer('Roll No.', readonly=False)

    _sql_constraints = [('roll_no_uniq', 'unique(roll_no)', 'This Roll already exists !'),
                        ('pid_uniq', 'unique(pid)', 'This Id already exists !')]
