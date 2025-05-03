# -*- coding: utf-8 -*-
{
    'name': "Bista CRM",

    'description': """
Long description of module's purpose
    """,

    'author': "Jainish",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'sale', 'sale_crm', 'mrp'],


    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'data/default_stages.xml',
        'views/crm_lead.xml',
        'views/crm_probability_stage.xml',
        'views/sale_order.xml',
        'views/product_product.xml',
        'wizards/add_num_wizard.xml',
        'views/mrp_production.xml',
    ],
    'application' : True,
}

