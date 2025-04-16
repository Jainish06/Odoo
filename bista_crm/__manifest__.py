# -*- coding: utf-8 -*-
{
    'name': "Bista CRM",

    'description': """
Long description of module's purpose
    """,

    'author': "Jainish",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'crm'],


    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead.xml',
    ],
    'application' : True,
}

