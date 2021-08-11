{
    'name': 'daily_purchase_statement',
    'version': '14.0',
    'author': 'Nova',
    'website': '',
    'depends': ['base', 'account'],
    'license': 'LGPL-3',
    'category': 'Sales',
    'data': [
        'security/ir.model.access.csv',
        'wizards/daily_purchase_statement_wizard.xml',
        'reports/daily_purchase_statement_report.xml',
        'reports/daily_purchase_statement_template.xml',
    ],
    'images': ['static/description/sale-report-banner.png'],
}
