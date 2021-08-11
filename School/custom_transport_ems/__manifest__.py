# -*- coding: utf-8 -*-
{
    'name': "custom_transport_ems",
    'author': "Nova",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'school', 'school_transport'],

    # always loaded
    'data': [
        'report/participants.xml',
        'report/report_view.xml',
        'views/inherited_transport.xml',
    ],
}
