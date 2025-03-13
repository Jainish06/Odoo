from odoo import fields, models

class DoctorDetails(models.Model):
    _name = 'doctor.details'
    _description = 'Doctor Details'

    name = fields.Char('Doctor name', required = True)
    designation = fields.Char('Designation', required = True)
    contact_no = fields.Char('Phone number', required = True)
    department_id = fields.Many2one('departments', 'Department')
    patient_ids = fields.One2many('patient.details', 'doctor_id')
    appointment_ids = fields.One2many('appointment.details', 'doctor_appointment_id')
    # wizard_ids = fields.One2many('doctor.list.wizard', 'doctor_id')