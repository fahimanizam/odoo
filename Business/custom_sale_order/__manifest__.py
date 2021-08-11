# -*- coding: utf-8 -*-
{
    'name': "custom_sale_order",
    'author': "Nova",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'views/inherited_sale.xml',
    ],
}
