# -*- coding: utf-8 -*-
{
    'name': "daily_sale_report",
    'author': "Nova",
    'website': "",
    'category': 'Sale',
    'version': '14.0',
    "license": "AGPL-3",
    'images': ['static/description/3.png'],
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/daily_wizard_view.xml',
        'reports/daily_sale_template.xml',
        'reports/template_report.xml',
    ],

    'qweb': [
        'static/src/xml/report_tmpl.xml'],

}
