# -*- coding: utf-8 -*-
import base64
import json
import requests
from datetime import datetime
from odoo.osv import expression
from odoo import http, fields
from odoo.http import request


# ----------------------------------------------------------
# AnswerSubmission Class for maintaining website
# ----------------------------------------------------------
# class AnswerSubmission(http.Controller):
#     print("Hello world")

# class NewsCarousel(http.Controller):
#     print("Hello World")
#     # @http.route(auth='public')
#     def index(self, **kw):
#         all_news = http.request.env['news.carousel']
#         return {
#             'all_news': all_news.search([])
#         }

@http.route(auth='public')
def render_posts(self, **kw):
    posts = request.env['blog.post']
    return http.request.render('news_carousel.inherited_template_header_default', {
        'posts': posts.search([])
    })


# @http.route(['/'], type='json', auth='public', website=True)
# def render_posts(self, domain, limit=None, order='published_date desc'):
#     dom = expression.AND([
#         [('website_published', '=', True), ('post_date', '<=', fields.Datetime.now())],
#         request.website.website_domain()
#     ])
#     if domain:
#         dom = expression.AND([dom, domain])
#     posts = request.env['blog.post'].search(dom, limit=limit, order=order)
#     return http.request.render('news_carousel.inherited_template_header_default',{'posts': posts})
    # return request.website.viewref(template)._render({'posts': posts})


# Answer Submission method
    # @http.route('/answer/submission', type='http', auth='public', website=True)
    # def answer_submission(self, **kw):
    #     exam_session_ids = request.env['exam.session'].sudo().search([])
    #     return http.request.render('emis_exam_session.template_student_input', {
    #         'exam_session_ids': exam_session_ids,
    #     })

    # Submission creating method
    # @http.route('/create/submission', type='http', auth="public", website=True)
    # def create_submission(self, **kw):
    #     response = {
    #         "status": False,
    #         "message": ''
    #     }
    #     kw.update({
    #         'department_name': kw.get('department_name'),
    #         'semester_name': kw.get('semester_name'),
    #         'college_name': kw.get('college_name'),
    #         'course_name': kw.get('course_name'),
    #         'course_code': kw.get('course_code'),
    #         # --------------
    #         'name': kw.get('name'),
    #         'nu_roll_no': kw.get('nu_roll_no'),
    #         'nu_reg_no': kw.get('nu_reg_no'),
    #     })
    #     if kw.get('attachment'):
    #         kw.update({
    #             'attachment': base64.b64encode(kw.get('attachment').read())
    #         })
    #     if kw.get('student_image'):
    #         kw.update({
    #             'student_image': base64.b64encode(kw.get('student_image').read())
    #         })
    #     if kw.get('admit_card'):
    #         kw.update({
    #             'admit_card': base64.b64encode(kw.get('admit_card').read())
    #         })
    #
    #     answer_submission = request.env['student.input'].sudo().create(kw)
    #     if answer_submission:
    #         response.update({
    #             "status": True,
    #             "message": 'Thanks! File Submitted successfully.'
    #         })
    #         return json.dumps(response)
    #     else:
    #         response.update({
    #             "status": False,
    #             "message": 'Sorry, Some problem occurred. Please try again later.'
    #         })
    #         return json.dumps(response)
