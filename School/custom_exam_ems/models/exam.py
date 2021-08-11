# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


# ------------------------------------
# Custom Exam Result Class
# ------------------------------------
class CustomExamResult(models.Model):
    _inherit = 'exam.result'

    @api.depends('result_ids', 'grade_system')
    def _compute_gpa(self):
        '''Method to compute gpa'''
        for rec in self:
            if rec.result_ids:
                nos = len(rec.result_ids)
                total_points = 0
                group_subject_result_ids = []
                for r in rec.result_ids:
                    if r.subject_id.is_grouped:
                        nos -= 1
                        group_subject_result_ids.append(r)
                    else:
                        grade = r.grade_line_id.grade
                        for g in rec.grade_system.grade_ids:
                            if grade == g.grade:
                                total_points += g.grade_point
                print('Total Points Before', total_points)
                for gs in group_subject_result_ids:
                    if gs.subject_id.is_grouped:
                        group_subject_total_percentage = gs.total_percentage
                        group_subject = gs.subject_id.group_subject
                        nogs = 1
                        for g in group_subject_result_ids:
                            if g.subject_id == group_subject:
                                nogs += 1
                                group_subject_total_percentage += g.total_percentage
                                group_subject_result_ids.remove(g)
                        group_avg = group_subject_total_percentage / nogs
                        nos += 1

                        for gr in rec.grade_system.grade_ids:
                            if group_avg >= gr.from_mark and group_avg <= gr.to_mark:
                                total_points += gr.grade_point
                                print("inside", total_points)

                        print('Group AVG', group_avg)
                        print('nos', nos)
                print('Total Points After', total_points)
                if total_points > 0:
                    gpa = total_points / nos
                    rec.gpa = round(gpa, 2)
                else:
                    rec.gpa = 0

    result_ids = fields.One2many(
        "exam.subject", "exam_id", "Exam Subjects", help="Select exam subjects",
    )
    grade_system = fields.Many2one(
        "grade.master", "Grade System", help="Grade System selected"
    )
    gpa = fields.Float(string="GPA", compute='_compute_gpa')
    board_standard = fields.Boolean(related='standard_id.board_standard')
    ssc_standard = fields.Boolean(related='standard_id.ssc_standard')


# ------------------------------------
# Custom School Standard Class
# ------------------------------------
class CustomSchoolStandard(models.Model):
    _inherit = 'school.standard'

    board_standard = fields.Boolean('Board Standard', default=False)
    ssc_standard = fields.Boolean('SSC Board Standard', default=False)


# ------------------------------------
# Custom Exam Subject Class
# ------------------------------------
class CustomExamSubject(models.Model):
    _inherit = "exam.subject"

    board_standard = fields.Boolean(related='exam_id.standard_id.board_standard')

    group_subject_number = fields.Float("Group Subject Number", compute='_compute_subject_number')
    group_subject_grade_line_id = fields.Many2one('grade.line', "Grade", compute='_compute_group_grade')
    group_subject_gpa = fields.Float('Group Subject GPA', compute="_compute_group_subject_gpa")

    @api.depends('exam_id', 'group_subject_grade_line_id')
    def _compute_group_subject_gpa(self):
        for rec in self:
            total_points = 0
            grade = rec.group_subject_grade_line_id.grade
            for g in rec.exam_id.grade_system.grade_ids:
                if grade == g.grade:
                    total_points += g.grade_point
            if total_points > 0:
                gpa = total_points
                rec.group_subject_gpa = round(gpa, 2)
            else:
                rec.group_subject_gpa = 0

    @api.depends('exam_id', 'group_subject_number', 'marks_reeval')
    def _compute_group_grade(self):
        self.group_subject_grade_line_id = ""
        for rec in self:
            grade_lines = rec.exam_id.grade_system.grade_ids
            if rec.subject_id.is_grouped:
                if rec.group_subject_number > 0:
                    marks_per = ((100 * rec.group_subject_number) / rec.maximum_marks)
                    if (rec.exam_id and rec.exam_id.student_id and grade_lines):
                        flag = False
                        for grade_id in grade_lines:
                            if marks_per >= grade_id.from_mark and marks_per <= grade_id.to_mark:
                                rec.group_subject_grade_line_id = grade_id
                                flag = True
                        if not flag:
                            raise ValidationError(_('''Obtain marks percentage is
                                out of range according to
                                selected grading system.
                                Please ensure the marks or grading system'''))
                else:
                    rec.group_subject_grade_line_id = ""

    @api.depends('subject_id')
    def _compute_subject_number(self):
        for rec in self:
            total_number = 0.0
            group_subject = []
            if rec.subject_id.is_grouped:
                vals = {
                    'code': rec.subject_id.group_code,
                    'sub1': rec.subject_id,
                    'sub2': rec.subject_id.group_subject
                }
                group_subject.append(vals)
                for sub in group_subject:
                    for r in rec.exam_id.result_ids:
                        if sub['sub2'] == r.subject_id:
                            total_number += ((rec.obtain_marks + r.obtain_marks) / 2)
                print(total_number)
            rec.group_subject_number = total_number

    @api.constrains('subject_id', 'terms', 'cq_marks', 'ct_marks', 'mcq_marks', 'practical_marks', 'obtain_marks',
                    'marks_reeval')
    def _validate_marks(self):
        for rec in self:
            board_standard = rec.exam_id.standard_id.board_standard
            # ct_max = rec.subject_id.ct_maximum_marks
            cq_max = rec.subject_id.cq_maximum_marks
            mcq_max = rec.subject_id.mcq_maximum_marks
            practical_max = rec.subject_id.practical_maximum_marks
            terms_max = rec.maximum_marks
            if board_standard == False:
                sba_max = (rec.subject_id.maximum_marks * 20) / 100
                if (rec.sba_marks > sba_max):
                    raise ValidationError(_('''The S.B.A marks
                                    should not exceed 20%% of maximum marks!
                                    N.B: The 20%% of Maximum Marks is %d''' % sba_max))
            ct_max = (rec.subject_id.maximum_marks * 20) / 100
            if rec.obtain_marks > rec.maximum_marks:
                raise ValidationError(_('''The obtained marks
                    should not exceed maximum marks!'''))
            if (rec.marks_reeval > rec.maximum_marks):
                raise ValidationError(_('''The revaluation marks
                    should not exceed maximum marks!'''))
            if (rec.terms > terms_max):
                raise ValidationError(_('''The terms marks
                    should not exceed terms maximum marks!
                    N.B: The Terms Maximum Marks is %d''' % terms_max))
            if (rec.ct_marks > ct_max):
                raise ValidationError(_('''The CT marks
                                    should not exceed 20%% of maximum marks!
                                    N.B: The 20%% of Maximum Marks is %d''' % ct_max))
            if rec.subject_id.is_cq:
                if (rec.cq_marks > cq_max):
                    raise ValidationError(_('''The CT marks
                                    should not exceed cq of maximum marks!
                                    N.B: The cq of Maximum Marks is %d''' % cq_max))
            if rec.subject_id.is_mcq:
                if (rec.mcq_marks > mcq_max):
                    raise ValidationError(_('''The CT marks
                                    should not exceed mcq of maximum marks!
                                    N.B: The mcq of Maximum Marks is %d''' % mcq_max))
            if rec.subject_id.is_practical:
                if (rec.practical_marks > practical_max):
                    raise ValidationError(_('''The CT marks
                                    should not exceed practical of maximum marks!
                                    N.B: The practical of Maximum Marks is %d''' % practical_max))

    @api.depends('mcq_marks', 'cq_marks', 'practical_marks')
    def _compute_total_exam_marks(self):
        for rec in self:
            total_exam_marks = 0.0
            if rec.mcq_marks:
                total_exam_marks += rec.mcq_marks
            if rec.cq_marks:
                total_exam_marks += rec.cq_marks
            if rec.practical_marks:
                total_exam_marks += rec.practical_marks
            rec.total_exam_marks = total_exam_marks

    @api.depends('total_exam_marks', 'sba_marks')
    def _convert_term_marks(self):
        for rec in self:
            if rec.exam_id.standard_id.ssc_standard:
                rec.terms = rec.total_exam_marks if rec.total_exam_marks > 0 else 0

    @api.depends('sba_marks', 'ct_marks', 'terms')
    def _compute_obtain_marks(self):
        for rec in self:
            if rec.exam_id.standard_id.board_standard or rec.exam_id.standard_id.ssc_standard:
                rec.obtain_marks = round((rec.terms * .8) + rec.ct_marks)
            else:
                additional_marks = ((rec.sba_marks + rec.ct_marks)/2)
                rec.obtain_marks = round((rec.terms * .8) + additional_marks)

    @api.depends('exam_id', 'grade_line_id')
    def _compute_gpa(self):
        for rec in self:
            total_points = 0
            grade = rec.grade_line_id.grade
            for g in rec.exam_id.grade_system.grade_ids:
                if grade == g.grade:
                    total_points += g.grade_point
            if total_points > 0:
                gpa = total_points
                rec.gpa = round(gpa, 2)
            else:
                rec.gpa = 0

    cq_marks = fields.Float("CQ", states={'ssc/hsc': [('readonly', True)]})
    mcq_marks = fields.Float("MCQ")
    practical_marks = fields.Float("Practical")
    gpa = fields.Float('GPA', compute="_compute_gpa")

    total_exam_marks = fields.Float("Total", compute='_compute_total_exam_marks', store=True)
    grade_line_id = fields.Many2one('grade.line', "Letter Grade", compute='_compute_grade')
    ct_marks = fields.Float("Class Test 20%")
    terms = fields.Float("Term Exam", compute='_convert_term_marks', store=True)
