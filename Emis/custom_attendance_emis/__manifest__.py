# -*- coding: utf-8 -*-
{
    'name': "custom_attendance_emis",
    'author': "Nova",
    'website': "",
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_core', 'openeducat_attendance','education_erp_1'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/inherited_daily_attendance.xml',
    ],
}
