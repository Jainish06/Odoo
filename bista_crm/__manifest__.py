# -*- coding: utf-8 -*-
{
    'name': "Bista CRM",

    'description': """
Long description of module's purpose
    """,

    'author': "Jainish",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'sale', 'sale_crm'],


    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'data/default_stages.xml',
        'views/crm_lead.xml',
        'views/crm_probability_stage.xml',
        'views/sale_order.xml'
    ],
    'application' : True,
}

