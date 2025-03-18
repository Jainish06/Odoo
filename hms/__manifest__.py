# -*- coding: utf-8 -*-

{
    'name': 'Hospital Management System',
    'version': '1.1',
    'category': '',
    'summary': 'HMS',
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/doctor_details.xml',
        'views/patient_details.xml',
        'views/department.xml',
        'views/staff_details.xml',
        'views/insurance_details.xml',
        'views/appointment_details.xml',
        'wizards/doctor_list_wizard.xml',
        'data/ir_patient_sequence.xml',
        'data/ir_appointment_sequence.xml',
        'data/ir_doctor_sequence.xml',
        'data/ir_cron.xml',
        'views/prescription_details.xml',
        'views/prescription_line.xml'
        ],
    'application' : True
}