from odoo import fields, models, api
from odoo.exceptions import UserError
import math

BLOOD_GROUP = [('A+', 'A+ve'),
                ('B+', 'B+ve'),
                ('O+', 'O+ve'),
                ('AB+', 'AB+ve'),
                ('A-', 'A-ve'),
                ('B-', 'B-ve'),
                ('O-', 'O-ve'),
                ('AB-', 'AB-ve')]


class PatientDetails(models.Model):
    _name = 'patient.details'
    _description = 'Patient Details'

    patient_code = fields.Char(string="Patient ID", copy=False, readonly=True, index=True, default="New")
    name = fields.Char('Patient name', required = True)
    contact_no = fields.Char('Phone number', required = True)
    email = fields.Char(string="Email")
    blood_group = fields.Selection(BLOOD_GROUP, string="Blood Group", required=True)
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    age = fields.Char(string="Age")
    main_complain = fields.Char('Main Complain', required=True)
    doctor_id = fields.Many2one('doctor.details', 'Doctor assigned')
    insurance_id = fields.Many2one('insurance.details', 'Insurance used')

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val.update({'patient_code' : self.env['ir.sequence'].next_by_code('patient.details') })
        res = super(PatientDetails, self).create(vals_list)
        return res

    @api.constrains('contact_no','app_date_time')
    def check_phone(self):
        for record in self:
            if record.contact_no and len(record.contact_no) < 10:
                raise UserError("Phone number should be minimum 10 digits")

            # check no duplicate phone number
            patient_ids = self.env['patient.details'].search_count([('contact_no', '=', record.contact_no), ('id', '!=', record.id)])
            if patient_ids:
                raise UserError("Phone number already exists")

    @api.constrains('date_of_birth')
    def check_dob(self):
        for record in self:
            if record.date_of_birth >= fields.Date.today():
                raise UserError("Invalid date.")

    def action_open_appointment_form(self):
        view_id = self.env.ref('hms.appointment_details_form_view').id
        print("view_id", view_id)
        return {
            'name': 'Appointments',
            'view_mode': 'form',
            'res_model': 'appointment.details',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    def action_calculate_age(self):
        current_date = fields.Date.today()
        age = str(current_date - self.date_of_birth)
        age = age.split(',')
        age = age[0]
        if age<'30':
            self.age = age
        elif age>='30':
            self.age = str(math.floor((int(age)%30)))

