# -*- coding: utf-8 -*-
{
    'name': "custom_customer_vendor",
    'author': "Nova",
    'website': "",
    'version': '0.1',
    'depends': ['base', 'account', 'sale', 'purchase', 'stock', 'bispro_partner_filter'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/inherited_res_partner.xml',
    ],
}
