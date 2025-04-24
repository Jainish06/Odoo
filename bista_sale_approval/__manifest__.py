# -*- coding: utf-8 -*-
{
    'name': "Bista Sale Approval",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Jainish",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['crm', 'sale_crm', 'purchase'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/email_template.xml',
        'views/res_config_setting.xml',
        'views/sale_order.xml',
        'views/purchase_order.xml'
    ],
    'application' : True,
}

