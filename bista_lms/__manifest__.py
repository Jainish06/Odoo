# -*- coding: utf-8 -*-
{
    'name': "Loan Management System",


    'description': """
    Loan and EMI managment.
    """,

    'author': "Jainish Pathak",

    'version': '0.1',

    'depends': ['base', 'account'],

    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        'data/email_template.xml',
        'views/loan_details.xml',
        'views/loan_interest_rate.xml',
        'views/loan_emi_lines.xml',
        'views/account_move.xml',
        'views/loan_approver_team.xml',
    ],

    'application' : True,
}

