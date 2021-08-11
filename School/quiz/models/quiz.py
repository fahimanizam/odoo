import base64
from odoo import api, fields, models
from odoo.exceptions import ValidationError, except_orm, UserError
from odoo.addons.survey.models.survey_user import SurveyUserInput as OriginalSurveyUserInput
from odoo.addons.survey.tests.common import SurveyCase as SurveyCase
from odoo.addons.survey.models.survey_survey import Survey as OriginalSurvey


# def _create_answer(self, user=False, partner=False, email=False, test_entry=False, check_attempts=True,
#                    **additional_vals):
#     """ Main entry point to get a token back or create a new one. This method
#     does check for current user access in order to explicitely validate
#     security.
#
#       :param user: target user asking for a token; it might be void or a
#                    public user in which case an email is welcomed;
#       :param email: email of the person asking the token is no user exists;
#     """
#     self.check_access_rights('read')
#     self.check_access_rule('read')
#
#     user_inputs = self.env['survey.user_input']
#     for survey in self:
#         if partner and not user and partner.user_ids:
#             user = partner.user_ids[0]
#
#         invite_token = additional_vals.pop('invite_token', False)
#         survey._check_answer_creation(user, partner, email, test_entry=test_entry, check_attempts=check_attempts,
#                                       invite_token=invite_token)
#         answer_vals = {
#             'survey_id': survey.id,
#             'test_entry': test_entry,
#             'is_session_answer': survey.session_state in ['ready', 'in_progress']
#         }
#         if survey.session_state == 'in_progress':
#             # if the session is already in progress, the answer skips the 'new' state
#             answer_vals.update({
#                 'state': 'in_progress',
#                 'start_datetime': fields.Datetime.now(),
#             })
#         if user and not user._is_public():
#             answer_vals['partner_id'] = user.partner_id.id
#             answer_vals['email'] = user.email
#             answer_vals['nickname'] = user.name
#         elif partner:
#             answer_vals['partner_id'] = partner.id
#             answer_vals['email'] = partner.email
#             answer_vals['nickname'] = partner.name
#         else:
#             answer_vals['email'] = email
#             answer_vals['nickname'] = email
#
#         if invite_token:
#             answer_vals['invite_token'] = invite_token
#         elif survey.is_attempts_limited and survey.access_mode != 'public':
#             # attempts limited: create a new invite_token
#             # exception made for 'public' access_mode since the attempts pool is global because answers are
#             # created every time the user lands on '/start'
#             answer_vals['invite_token'] = self.env['survey.user_input']._generate_invite_token()
#
#         answer_vals.update(additional_vals)
#         user_inputs += user_inputs.create(answer_vals)
#
#     for question in self.mapped('question_ids').filtered(
#         lambda q: q.question_type == 'char_box' and (q.save_as_email or q.save_as_nickname)):
#         for user_input in user_inputs:
#             if question.save_as_email and user_input.email:
#                 user_input.save_lines(question, user_input.email)
#             if question.save_as_nickname and user_input.nickname:
#                 user_input.save_lines(question, user_input.nickname)
#
#     return user_inputs
#
#
# OriginalSurvey._create_answer = _create_answer
#
#
# def _add_answer(self, survey, student, **kwargs):
#     base_avals = {
#         'survey_id': survey.id,
#         'student_id': student.id if student else False,
#         'email': kwargs.pop('email', False),
#     }
#     base_avals.update(kwargs)
#     return self.env['survey.user_input'].create(base_avals)
#
#
# SurveyCase._add_answer = _add_answer
#
#
# @api.depends('state', 'test_entry', 'survey_id.is_attempts_limited', 'student_id', 'email', 'invite_token')
# def _compute_attempts_number(self):
#     attempts_to_compute = self.filtered(
#         lambda
#             user_input: user_input.state == 'done' and not user_input.test_entry and user_input.survey_id.is_attempts_limited
#     )
#
#     for user_input in (self - attempts_to_compute):
#         user_input.attempts_number = 1
#
#     if attempts_to_compute:
#         self.env.cr.execute("""SELECT user_input.id, (COUNT(previous_user_input.id) + 1) AS attempts_number
#                 FROM survey_user_input user_input
#                 LEFT OUTER JOIN survey_user_input previous_user_input
#                 ON user_input.survey_id = previous_user_input.survey_id
#                 AND previous_user_input.state = 'done'
#                 AND previous_user_input.test_entry IS NOT TRUE
#                 AND previous_user_input.id < user_input.id
#                 AND (user_input.invite_token IS NULL OR user_input.invite_token = previous_user_input.invite_token)
#                 AND (user_input.student_id = previous_user_input.student_id)
#                 WHERE user_input.id IN %s
#                 GROUP BY user_input.id;
#         """, (tuple(attempts_to_compute.ids),))
#
#         attempts_count_results = self.env.cr.dictfetchall()
#
#         for user_input in attempts_to_compute:
#             attempts_number = 1
#             for attempts_count_result in attempts_count_results:
#                 if attempts_count_result['id'] == user_input.id:
#                     attempts_number = attempts_count_result['attempts_number']
#                     break
#
#             user_input.attempts_number = attempts_number
#
#
# OriginalSurveyUserInput._compute_attempts_number = _compute_attempts_number
#
#
# def action_resend(self):
#     students = self.env['student.student']
#     for user_answer in self:
#         if user_answer.student_id:
#             if user_answer.standard_id.student_id:
#                 students |= user_answer.student_id
#
#     return self.survey_id.with_context(
#         default_existing_mode='resend',
#         default_student_ids=students.ids,
#         # default_emails=','.join(emails)
#     ).action_send_survey()
#
#
# OriginalSurveyUserInput.action_resend = action_resend


def save_lines(self, question, answer, comment=None):
    """ Save answers to questions, depending on question type

        If an answer already exists for question and user_input_id, it will be
        overwritten (or deleted for 'choice' questions) (in order to maintain data consistency).
    """
    old_answers = self.env['survey.user_input.line'].search([
        ('user_input_id', '=', self.id),
        ('question_id', '=', question.id)
    ])

    if question.question_type in ['char_box', 'text_box', 'numerical_box', 'date', 'datetime', 'upload_file']:
        self._save_line_simple_answer(question, old_answers, answer)
        if question.save_as_email and answer:
            self.write({'email': answer})
        if question.save_as_nickname and answer:
            self.write({'nickname': answer})

    elif question.question_type in ['simple_choice', 'multiple_choice']:
        self._save_line_choice(question, old_answers, answer, comment)
    elif question.question_type == 'matrix':
        self._save_line_matrix(question, old_answers, answer, comment)
    else:
        raise AttributeError(question.question_type + ": This type of question has no saving function")


OriginalSurveyUserInput.save_lines = save_lines


class SchoolStandard(models.Model):
    _name = "school.standard"
    _inherit = "school.standard"
    _rec_name = "survey_ids"

    survey_ids = fields.Many2many(
        "survey.survey",
        "school_survey_standard_rel",
        "survey_id",
        "standard_id",
        "Survey",
        help="Select survey for the standard",
    )


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    title = fields.Char('Quiz Title', required=True, translate=True)

    school_id = fields.Many2one('school.school', 'School',
                                help='Select school')
    standard_id = fields.Many2one(
        "school.standard", "Standard", help="Select standard for exam"
    )
    subject_id = fields.Many2one(
        "subject.subject", "Subject Name", help="Select subject for exam"
    )
    survey_input_ids = fields.One2many("survey.user_input", 'survey_id', string="Student info",
                                       domain="[('is_student','=',True)]")
    # survey_input = fields.Many2one("survey.user_input", string="Survey Input info")
    quiz_start = fields.Datetime("Quiz Start Date", default=fields.Datetime.now(), help="Select quiz start date")
    # quiz_marks = fields.Integer(
    #     "Quiz Mark", help="Minimum Marks of exam"
    # )
    pass_marks = fields.Integer(
        "Pass Mark", help="Maximum Marks of Exam"
    )

    quiz_type = fields.Selection([
        ('general', 'General Quiz'),
        ('academic', 'Academic Quiz')], default='general')

    student_answer_count = fields.Integer(
        'Student Answer', compute='_compute_student_answer',
        help='Number of student answered the question')

    def _compute_student_answer(self):
        self.student_answer_count = 0
        for servey in self:
            servey.student_answer_count = self.env['survey.user_input'].search_count(
                [('survey_id', '=', servey.id), ('is_student', '=', True)])


class SchoolSurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    survey_id = fields.Many2one('survey.survey', string='Quiz', required=True, readonly=True, ondelete='cascade')
    scoring_type = fields.Selection(string="Marks", related="survey_id.scoring_type")
    start_datetime = fields.Datetime('Start date and time', readonly=True)
    deadline = fields.Datetime('Deadline', help="Datetime until customer can open the survey and submit answers")

    partner_id = fields.Many2one('res.partner', string='User name', readonly=True)
    student_id = fields.Many2one("student.student", string="Student Name", readonly=1, compute='compute_student_id')
    roll_no = fields.Char("Roll No", readonly=False)
    standard_id = fields.Many2one(
        "school.standard", "Standard", related='survey_id.standard_id', help="Select standard for quiz", readonly=True
    )

    is_student = fields.Boolean('IS student', default=False, readonly=1)

    # @api.depends('partner_id')
    def compute_student_id(self):
        self.student_id = 0
        for rec in self:
            if rec.standard_id:
                if rec.partner_id.id:
                    user = self.env['student.student'].search([("user_id.partner_id", "=", rec.partner_id.id)], limit=1)
                    if user.id:
                        rec.student_id = user.id
                        rec.roll_no = rec.student_id.roll_no
                        rec.is_student = True

    # @api.model
    # def create(self, vals):
    #     if vals.get('student_id'):
    #         student = self.env['student.student'].browse(vals.get('student_id'))
    #         vals.update({
    #             'roll_no': student.roll_no
    #         })
    #     return super(SchoolSurveyUserInput, self).create(vals)
    #
    # def write(self, vals):
    #     if vals.get('student_id'):
    #         student = self.env['student.student'].browse(vals.get('student_id'))
    #         vals.update({
    #             'roll_no': student.roll_no,
    #         })
    #     return super(SchoolSurveyUserInput, self).write(vals)


class SchoolSurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    answer_type = fields.Selection([
        ('text_box', 'Free Text'),
        ('char_box', 'Text'),
        ('numerical_box', 'Number'),
        ('upload_file', 'Upload File'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('suggestion', 'Suggestion')], string='Answer Type')

    file = fields.Binary('Upload file')
    file_type = fields.Selection([('image', 'image'), ('pdf', 'pdf')])

    @api.model
    def save_line_upload_file(self, user_input_id, question, post, answer_tag):
        vals = {
            'user_input_id': user_input_id,
            'question_id': question.id,
            'survey_id': question.survey_id.id,
            'skipped': False
        }
        file_name = str(post[answer_tag])
        file_type = file_name.find("('application/pdf')")
        image_type = file_name.find("('image/png')")
        if file_type > -1:
            vals.update({'file_type': 'pdf'})
        if image_type > -1:
            vals.update({'file_type': 'image'})

        if question.constr_mandatory:
            file = base64.encodebytes(post[answer_tag].read())
        else:
            file = base64.encodebytes(post[answer_tag].read()) if post[answer_tag] else None
        if answer_tag in post:
            vals.update({'answer_type': 'upload_file', 'file': file})
        else:
            vals.update({'answer_type': None, 'skipped': True})
        old_uil = self.search([
            ('user_input_id', '=', user_input_id),
            ('survey_id', '=', question.survey_id.id),
            ('question_id', '=', question.id)
        ])
        if old_uil:
            old_uil.write(vals)
        else:
            old_uil.create(vals)
        return True


class SchoolSurveyQuestion(models.Model):
    _inherit = "survey.question"

    question_attachment = fields.Binary('Question attachment')
    question_type = fields.Selection([
        ('text_box', 'Multiple Lines Text Box'),
        ('char_box', 'Single Line Text Box'),
        ('numerical_box', 'Numerical Value'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('simple_choice', 'Multiple choice: only one answer'),
        ('multiple_choice', 'Multiple choice: multiple answers allowed'),
        ('upload_file', 'Upload File'),
        ('matrix', 'Matrix')], string='Question Type',
        compute='_compute_question_type', readonly=False, store=True)
