# -*- coding: utf-8 -*-
{
    'name': "item_issue_report",
    'author': " Nova ",
    'website': "",
    'category': 'Sale',
    'version': '14.0',
    "license": "AGPL-3",
    'images': ['static/description/3.png'],
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/item_issue_register_wizard_view.xml',
        'reports/Item_issue_register_template.xml',
        'reports/Item_issue_register_report.xml',
    ],
    'qweb': [
        'static/src/xml/report_tmpl.xml'],

}
