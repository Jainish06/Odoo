# -*- coding: utf-8 -*-
{
    'name': "Bista Manufacturing",

    'description': '''Manusfactring task''',

    'author': "Jainish Pathak",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'mrp', 'sale', 'mrp_account'],

    'data': [
        'security/ir.model.access.csv',
        'views/mrp_production.xml',
        'wizards/mrp_report_wizard.xml',
        'wizards/mrp_replace_wizard.xml',
    ],
    'application' : True,
}

