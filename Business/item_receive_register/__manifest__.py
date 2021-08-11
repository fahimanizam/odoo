# -*- coding: utf-8 -*-
{
    'name': "item_receive_register",
    'author': " Nova ",
    'website': "",
    'category': 'Purchase',
    'version': '14.0',
    "license": "AGPL-3",
    'images': ['static/description/3.png'],
    'depends': ['base', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/item_receive_register_wizard_view.xml',
        'reports/item_receive_register_template.xml',
        'reports/item_receive_register_report.xml',
    ],
    'qweb': [
        'static/src/xml/report_tmpl.xml'],

}
