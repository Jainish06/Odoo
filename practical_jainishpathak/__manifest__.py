# -*- coding: utf-8 -*-
{
    'name': "Practical_JainishPathak",

    'description': """Evaluation 2 module
    """,

    'author': "Jainish Pathak",

    'version': '0.1',

    'depends': ['base', 'sale', 'stock'],

    # always loaded
    'data': [
        'data/pharmacy_default_values.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/email_tamplate.xml',
        'data/system_param.xml',
        'views/pharmacy_master.xml',
        'views/product_template.xml',
        'views/account_move.xml',
        'views/sale_order.xml',
        # 'views/stock_picking.xml',
        'views/mail_activity_schedule.xml',
        'views/res_config_setting.xml',
        'wizards/add_product_wizard.xml',
        'views/do_report_inherit_template.xml'
    ],

   'application' : True,
}

