# -*- coding: utf-8 -*-
{
    'name': "rma",

    'description': """
Long description of module's purpose
    """,

    'author': "Jainish",

    'category': 'Uncategorized',
    'version': '1.1',

    'depends': ['base', 'sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_rma.xml',
        'views/teams.xml'
    ],
    'application' : 'True',
}

