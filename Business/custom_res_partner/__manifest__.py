# -*- coding: utf-8 -*-
{
    'name': "custom_res_partner",
    'author': "Nova",
    'website': "",
    'version': '0.1',
    'depends': ['base','web_widget_timepicker','event'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/inherited_res_partner.xml',
        'views/inherited_event.xml',
    ],
}
