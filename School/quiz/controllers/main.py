import json
import logging
import werkzeug
from datetime import datetime
from math import ceil
from odoo.exceptions import UserError

from odoo import fields, http, SUPERUSER_ID, _
from odoo.http import request
from odoo.tools import ustr
from odoo.addons.survey.controllers.main import Survey
# from odoo.addons.survey.controllers.main import Survey as OriginalSurvey
from odoo.http import request
import html2text

_logger = logging.getLogger(__name__)

#
# @http.route(['/survey/<int:survey_id>/get_certification'], type='http', auth='user', methods=['GET'], website=True)
# def survey_get_certification(self, survey_id, **kwargs):
#     """ The certification document can be downloaded as long as the user has succeeded the certification """
#     survey = request.env['survey.survey'].sudo().search([
#         ('id', '=', survey_id),
#         ('certification', '=', True)
#     ])
#
#     if not survey:
#         # no certification found
#         return werkzeug.utils.redirect("/")
#
#     succeeded_attempt = request.env['survey.user_input'].sudo().search([
#         ('partner_id', '=', request.env.user.partner_id.id),
#         ('student_id', '=', request.env.user.student_id.id),
#         ('survey_id', '=', survey_id),
#         ('scoring_success', '=', True)
#     ], limit=1)
#
#     if not succeeded_attempt:
#         raise UserError(_("The user has not succeeded the certification"))
#
#     return self._generate_report(succeeded_attempt, download=True)
#
# OriginalSurvey.survey_get_certification = survey_get_certification

class WebsiteSurveyExtend(Survey):
    @http.route(['/survey/print/<model("survey.survey"):survey>',
                 '/survey/print/<model("survey.survey"):survey>/<string:survey_token>'],
                type='http', auth='public', website=True)
    def survey_print(self, survey, token=None, **post):
        '''Display an survey in printable view; if <token> is set, it will
        grab the answers of the user_input_id that has <token>.'''

        survey_question = request.env['survey.question']
        user_input = request.env['survey.user_input']
        user_input_line = request.env['survey.user_input.line']

        question_ids = survey_question.sudo().search([('type', '=', 'upload_file'), ('survey_id', '=', survey.id)])
        user_input_id = user_input.sudo().search([('token', '=', token), ('survey_id', '=', survey.id)])

        user_input_line_upload_file = []
        for question in question_ids:
            user_input_line = user_input_line.search([
                ('user_input_id', '=', user_input_id.id),
                ('survey_id', '=', survey.id),
                ('question_id', '=', question.id),
                ('answer_type', '=', 'upload_file')
            ])
            user_input_line_upload_file.append(user_input_line)
        return request.render('survey.survey_page_print',
                              {'survey': survey,
                               'token': token,
                               'page_nr': 0,
                               'quizz_correction': True if survey.quizz_mode and token else False,
                               'user_input_line_upload_file': user_input_line_upload_file})

    @http.route('/test/path', type='http', methods=['POST'], auth="public", website=True, csrf=False)
    def test_path(self, **kw):
        # here in kw you can get the inputted value
        print
        kw['name']
