# -*- coding: utf-8 -*-
{
    'name': "custom_event_ems",
    'author': "Nova",
    'website': "",
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'school', 'event', 'website_event'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/inherited_event.xml',
    ],
}
