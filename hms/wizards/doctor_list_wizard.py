from odoo import models, fields


class DoctorListWizard(models.TransientModel):
    _name = 'doctor.list.wizard'
    _description = 'School Opening Wizard'

    doctor_ids = fields.Many2many('doctor.details', string='Doctors')

