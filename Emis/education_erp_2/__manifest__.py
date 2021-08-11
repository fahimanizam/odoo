# -*- coding: utf-8 -*-
{
    'name': "education_erp_2",
    'author': "Nova",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'account', 'crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/inherited_account_partner.xml',
        'views/inherited_base_partner.xml',
        'views/inherited_crm_partner.xml',
        'views/inherited_sale_partner.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
