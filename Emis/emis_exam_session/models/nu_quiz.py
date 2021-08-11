from datetime import datetime
import random
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError


class NuQuiz(models.Model):
    _name = 'nu.quiz'

    name = fields.Char('Name of Quiz', required=True)
    time_limit = fields.Float("Time limit (minutes)", default=10)
    attempts_limit = fields.Integer('Number of attempts', default=1)
    # Inherited ids
    department_id = fields.Many2one("op.department", string="Department")
    faculty_id = fields.Many2one("edu.faculty", string="Faculty")
    course_id = fields.Many2one("op.course", string="Semester/Year")
    batch_id = fields.Many2one("op.batch", string="Batch")
    subject_id = fields.Many2one("op.subject", string="Subject")
    participant_ids = fields.Many2many('res.users', string="Participants")

    use_date_range = fields.Boolean("Use Publish Date Range")
    start_datetime = fields.Datetime("Start")
    end_datetime = fields.Datetime("End")

    def select_participants(self):
        if not self.course_id:
            raise UserError(_("Please Select Course First."))
        else:
            all_student = self.env['op.student'].search([('course_id', '=', self.course_id.id)])
            allowed_students = list()
            for student in all_student:
                allowed_students.append(student.user_id.id)
            self.participant_ids = [(6, 0, allowed_students)]


    # Question Bank

    question_bank_ids = fields.Many2many("op.question.bank", string="Question Banks")
    temp_bank_id = fields.Many2one("op.question.bank", string="Temp Bank")
    total_marks = fields.Float(string="Total Marks")
    computed_total_marks = fields.Float(string="Total Marks", compute="_get_total_marks_for_random")

    def get_total_marks_to_portal(self):
        return self.total_marks or self.computed_total_marks

    # @api.onchange('question_bank_ids')
    # def onchange_question_bank_ids(self):
    #     if len(self.question_bank_ids.ids) == 1:
    #         self.temp_bank_id = self.question_bank_ids.ids[0]
    #     else:
    #         self.temp_bank_id = False



    # def _get_total_marks_for_random(self):
    #     total_marks = 0
    #     for line in self.config_ids:
    #         total_marks = total_marks + (line.no_of_question * line.question_marks)
    #     self.computed_total_marks = total_marks
