# -*- coding: utf-8 -*-
{
    'name': "custom_product_partner",
    'author': "Nova",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'views/inherited_product.xml',
    ],
}
