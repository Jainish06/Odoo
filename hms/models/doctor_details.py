from odoo import fields, models, api
from odoo.exceptions import UserError


class DoctorDetails(models.Model):
    _name = 'doctor.details'
    _description = 'Doctor Details'

    doctor_code = fields.Char('Doctor Id', copy=False, readonly=True, index=True, default="New")
    name = fields.Char('Doctor name', required = True)
    designation = fields.Char('Designation', required = True)
    contact_no = fields.Char('Phone number', required = True)
    department_id = fields.Many2one('departments', 'Department')
    patient_ids = fields.One2many('patient.details', 'doctor_id')
    appointment_ids = fields.One2many('appointment.details', 'doctor_appointment_id')

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val.update({'doctor_code': self.env['ir.sequence'].next_by_code('doctor.details')})
        res = super(DoctorDetails, self).create(vals_list)
        return res

    @api.constrains('contact_no')
    def check_phone(self):
        for record in self:
            if record.contact_no and len(record.contact_no) < 10:
                raise UserError("Phone number should be minimum 10 digits")

            # check no duplicate phone number
            patient_ids = self.env['doctor.details'].search_count(
                [('contact_no', '=', record.contact_no), ('id', '!=', record.id)])
            if patient_ids:
                raise UserError("Phone number already exists")