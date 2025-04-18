# -*- coding: utf-8 -*-

{
    'name': 'Hospital Management System',
    'version': '1.1',
    'category': '',
    'summary': 'HMS',
    'depends': ['base', 'product', 'account', 'sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/appointment_email_template.xml',
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
        'views/prescription_line.xml',
        'views/stock_picking.xml',
        'views/sale_order.xml',
        'views/prescription_report_template.xml',
        'views/report.xml',
        'views/product_template.xml',
        'wizards/quantity_update_wizard.xml',
        'views/sale_order_report_template.xml'
        ],
    'application' : True,
    # 'pre_init_hook': 'update_record_rule'
}