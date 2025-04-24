# -*- coding: utf-8 -*-
{
    'name': "rma",

    'description': """
Long description of module's purpose
    """,

    'author': "Jainish",

    'category': 'Uncategorized',
    'version': '1.1',

    'depends': ['base', 'sale', 'product'],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_rma.xml',
        'views/teams.xml',
        'wizards/rma_line_wizard.xml',
        'wizards/rma_invoice_wizard.xml'
    ],
    'application' : 'True',
}

