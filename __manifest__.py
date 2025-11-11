{
    'name': 'Fatura Entegrator',
    'version': '1.0.1',
    'summary': 'Fatura Entegratör ile sipariş ve fatura entegrasyonu (çoklu şirket).',
    'description': 'Fatura Entegratör API ile çoklu şirket bazında sipariş (sale.order) ve fatura (account.move) gönderimi, formalize ve PDF alma işlemleri.',
    'category': 'Accounting/Invoicing',
    'author': 'Your Company',
    'license': 'LGPL-3',
    'depends': ['base', 'sale_management', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_company_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/fe_invoice_views.xml',
    ],
    'application': False,
    'installable': True,
}

