# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


# ------------------------------------
# Custom Subject class
# ------------------------------------
class CustomSubjectSubject(models.Model):
    _inherit = 'subject.subject'

    @api.constrains('minimum_marks', 'maximum_marks', 'terms_minimum_marks', 'terms_maximum_marks')
    def _validate_marks(self):
        min_marks = self.minimum_marks
        max_marks = self.maximum_marks
        if max_marks <= 0:
            raise ValidationError(_('''Please enter a valid maximum mark!'''))
        terms_min_marks = self.terms_minimum_marks
        terms_max_marks = self.terms_maximum_marks
        eighty_percent_of_max_marks = (max_marks * 80) / 100
        if min_marks > max_marks:
            raise ValidationError(_('''The minimum marks
                            should not exceed maximum marks!'''))
        if terms_max_marks > eighty_percent_of_max_marks:
            raise ValidationError(_('''The maximum marks
                                        should not exceed the 60%% of maximum marks!
                                        N.B: 80%% of maximum marks is %d''' % eighty_percent_of_max_marks))
        if terms_min_marks > terms_max_marks:
            raise ValidationError(_('''The terms minimum marks
                            should not exceed terms maximum marks!'''))

    @api.depends('maximum_marks')
    def _compute_terms_max(self):
        for rec in self:
            max_marks = rec.maximum_marks
            eighty_percent_of_max_marks = (max_marks * 80) / 100
            rec.terms_maximum_marks = eighty_percent_of_max_marks

    # Converting term maximum into 80 from 60
    terms_maximum_marks = fields.Integer("Term Maximum marks", compute=_compute_terms_max)

    # Relationship between subject & standard
    standard_ids = fields.Many2many('school.standard', 'subject_standards_rel', 'standard_id', 'subject_id',
                                    string='Standards')

    # Group subject can be identified by these fields
    is_grouped = fields.Boolean("Is Grouped", default=False)
    group_code = fields.Char('Group Name')
    group_subject = fields.Many2one('subject.subject', 'Group Subject')

    # Ct Marks maximum & Minimum marks can be defined using these fields
    is_ct = fields.Boolean('Is CT', default=True, help='Check this if subject is CT.')
    ct_maximum_marks = fields.Integer("CT Maximum marks")
    ct_minimum_marks = fields.Integer("CT Minimum marks")

    # MCQ Marks maximum & Minimum marks can be defined using these fields
    is_mcq = fields.Boolean('Is MCQ', help='Check this if subject is MCQ.')
    mcq_maximum_marks = fields.Integer("MCQ Maximum marks")
    mcq_minimum_marks = fields.Integer("MCQ Minimum marks")

    # CQ Marks maximum & Minimum marks can be defined using these fields
    is_cq = fields.Boolean('Is CQ', help='Check this if subject is CQ.')
    cq_maximum_marks = fields.Integer("CQ Maximum marks")
    cq_minimum_marks = fields.Integer("CQ Minimum marks")

    # Practical Marks maximum & Minimum marks can be defined using these fields
    is_practical = fields.Boolean('Is Practical', help='Check this if subject is practical.')
    practical_maximum_marks = fields.Integer("Practical Maximum marks")
    practical_minimum_marks = fields.Integer("Practical Minimum marks")
