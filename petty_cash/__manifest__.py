# -*- coding: utf-8 -*-
{
    'name': "Petty Cash",
    'summary': """Sistem Kas Kecil""",

    'description': """
        Modul ini digunakan untuk menjalankan sistem pencatatan kas kecil
    """,
    'sequence': -100,
    'author': "Felis, Tugas Akhir",
    # 'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'sale', 'board', 'account', 'l10n_id'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/petty_cash_data.xml',
        'report/petty_cash_report.xml',
        'report/reports.xml',
        'views/accounting_view.xml',
        'views/inherit_accounting_view.xml',  
        'wizard/petty_cash_replenishment.xml',    
        'views/inherit_account_journal.xml',
        'views/menus.xml',
        'views/dashboard_view.xml',
        'views/res_config_settings_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'petty_cash/static/src/components/**/*.js',
            'petty_cash/static/src/components/**/*.xml',
            'petty_cash/static/src/components/**/*.scss',
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
