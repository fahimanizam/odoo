import collections
import json
import itertools
import operator

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class NuQuizQuestion(models.Model):
    _name = 'nu.quiz.question'

    # question generic data
    question = fields.Char('Question', required=True)
    question_marks = fields.Float('Question Mark', required=True)
    description = fields.Html(
        'Description', translate=True,
        help="Use this field to add additional explanations about question/picture")

    nu_quiz_id = fields.Many2one('nu.quiz', 'Quiz Id')
    page_id = fields.Many2one('nu.quiz.question', string='Page', compute="_compute_page_id", store=True)
    question_type = fields.Selection([
        ('text_box', 'Multiple Lines Text Box'),
        ('simple_choice', 'Multiple choice: only one answer'),
        ('multiple_choice', 'Multiple choice: multiple answers allowed')
    ], string='Question Type',
        compute='_compute_question_type', readonly=False, store=True)

    sequence = fields.Integer('Sequence', default=10)
    is_page = fields.Boolean('Is a page?')
    question_ids = fields.One2many('nu.quiz.question', string='Questions', compute="_compute_question_ids")

    random_questions_count = fields.Integer(
        'Random questions count', default=1,
        help="Used on randomized sections to take X random questions from all the questions of that section.")

    @api.depends('is_page')
    def _compute_question_type(self):
        for question in self:
            if not question.question_type or question.is_page:
                question.question_type = False

    @api.depends('nu_quiz_id.question_and_page_ids.is_page', 'nu_quiz_id.question_and_page_ids.sequence')
    def _compute_page_id(self):
        for question in self:
            if question.is_page:
                question.page_id = None
            else:
                page = None
                for q in question.nu_quiz_id.question_and_page_ids.sorted():
                    if q == question:
                        break
                    if q.is_page:
                        page = q
                question.page_id = page

    @api.depends('nu_quiz_id.question_and_page_ids.is_page', 'nu_quiz_id.question_and_page_ids.sequence')
    def _compute_question_ids(self):
        for question in self:
            if question.is_page:
                next_page_index = False
                for page in question.nu_quiz_id.page_ids:
                    if page._index() > question._index():
                        next_page_index = page._index()
                        break

                question.question_ids = question.nu_quiz_id.question_ids.filtered(
                    lambda q: q._index() > question._index() and (not next_page_index or q._index() < next_page_index)
                )
            else:
                question.question_ids = self.env['nu.quiz.question']

    def _index(self):
        self.ensure_one()
        return list(self.nu_quiz_id.question_and_page_ids).index(self)
