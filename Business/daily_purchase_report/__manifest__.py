# -*- coding: utf-8 -*-
{
    'name': "daily_purchase_report",
    'author': " Nova ",
    'website': "",
    'category': 'Purchase',
    'version': '14.0',
    "license": "AGPL-3",
    'images': ['static/description/3.png'],
    'depends': ['base', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/daily_purchase_wizard_view.xml',
        'reports/daily_purchase_template.xml',
        'reports/daily_purchase_report.xml',
    ],
    'qweb': [
        'static/src/xml/report_tmpl.xml'],

}
