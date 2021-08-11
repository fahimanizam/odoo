# -*- coding: utf-8 -*-
{
    'name': "custom_attendance",
    'author': "Nova",
    'website': "",
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'school', 'school_attendance'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/inherited_daily_attendance.xml',
    ],
}
