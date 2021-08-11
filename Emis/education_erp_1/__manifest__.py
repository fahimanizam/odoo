# -*- coding: utf-8 -*-


{
    'name': "education_erp_1",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Nova",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_core', 'openeducat_activity', 'account', 'nu_edu', 'openeducat_timetable'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/inherited_student_view.xml',
        'views/inherited_subject_view.xml',
        'views/inherited_course_view.xml',
        'views/inherited_faculty_view.xml',
        'views/inherited_core_view.xml',
        'wizard/custom_erp_wizard.xml',
        'wizard/inherited_timetable_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
