# -*- coding: utf-8 -*-
{
    'name': "custom_service",

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
    'depends': ['base', 'bureaucrat_helpdesk_lite','mobile_service_shop'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/event_security.xml',
        # 'report/additional_exam_report.xml',
        # 'report/report_view.xml',
        'views/inherited_service.xml',
    ],
}
