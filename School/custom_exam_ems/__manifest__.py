# -*- coding: utf-8 -*-
{
    'name': "custom_exam_ems",
    'author': "Nova",
    'website': "",

    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'school', 'exam', "signature"],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/additional_exam_report.xml',
        'report/all_additional_exam_report.xml',
        'report/exam_result_report_card_board_standard.xml',
        'report/exam_result_report_card.xml',
        'report/report_view.xml',
        'views/inherited_exam.xml',
        'views/all_additional_exam.xml',
    ],
}
