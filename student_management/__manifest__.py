# -*- coding: utf-8 -*-
{
    'name': "student_management",

    'summary': "Student Management System",

    'description': """
        Long description of module's purpose
    """,

    'author': "Jainish Pathak",

    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/res_student.xml',
        'views/subject_subject.xml',
        'views/tuition_fee_structure.xml',
        'views/res_partner.xml',
        'views/student_activity.xml',
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
    ],
    'application':'True',
}

