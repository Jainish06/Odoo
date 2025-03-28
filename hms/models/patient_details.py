import typing
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.addons.test_new_api.models.test_new_api import Selection
from odoo.api import ValuesType
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
AGE_CATEGORY = [('child', 'Child'), ('minor', 'Minor'), ('adult', 'Adult'), ('senior citizen', 'Senior Citizen')]
GUARDIAN_CATEGORY = [('parent', 'Parent'), ('sibling', 'Sibling'), ('relative', 'Relative'), ('friend', 'Friend'),('other', 'Other')]


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
    age_category = fields.Selection(AGE_CATEGORY, string="Age Category", required=True)
    guardian_type = fields.Selection(GUARDIAN_CATEGORY, string="Guardian Category")
    guardian_id = fields.Many2one('res.partner', 'Guardian Id')
    main_complain = fields.Char('Main Complain', required=True)
    doctor_id = fields.Many2one('doctor.details', 'Doctor assigned')
    appointment_ids = fields.One2many('appointment.details', 'patient_id', 'Appointments')
    insurance_id = fields.Many2one('insurance.details', 'Insurance used')
    weekly_visit = fields.Boolean('Weekly visit?')
    appointment_count = fields.Integer(compute="_compute_appointment_count", string="Appointment Count", store=True)
    prescription_count = fields.Integer(compute='_compute_prescription_count', string='Prescription Count')
    partner_id = fields.Many2one('res.partner', 'Patient Partner')

    @api.depends('appointment_ids.patient_id')
    def _compute_appointment_count(self):
        for patient in self:
            patient.appointment_count = self.env['appointment.details'].search_count([('patient_id', '=', patient.id)])

    @api.depends()
    def _compute_prescription_count(self):
        for patient in self:
            patient.prescription_count = self.env['prescription.details'].search_count([('patient_id', '=', patient.id)])

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            vals = {'name': val['name'], 'mobile': val['contact_no'], 'email': val['email']}
            rec = self.env['res.partner'].create(vals)
            val.update({'patient_code' : self.env['ir.sequence'].next_by_code('patient.details') })
            val.update({'partner_id': rec.id})
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

    @api.onchange('date_of_birth')
    def onchange_method(self):
        if self.date_of_birth:
            current_date = fields.Date.today()
            age_delta = relativedelta(current_date, self.date_of_birth)
            self.age = age_delta.years
            if age_delta.years <= 10:
                self.age_category = 'child'
            elif 10 < age_delta.years < 18:
                self.age_category = 'minor'
            elif 18 <= age_delta.years < 60:
                self.age_category = 'adult'
            else:
                self.age_category = 'senior citizen'


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
            'context': {'default_patient_id': self.id,}
        }

    def action_calculate_age(self):
        current_date = fields.Date.today()
        age_delta = relativedelta(current_date, self.date_of_birth)
        self.age = f"{age_delta.years} year(s) {age_delta.months} month(s) {age_delta.days} month(s)"

    def _count_no_of_patients(self):
        # This method will be called by a cron job
        patient_ids = self.env['patient.details'].search([('age', '>', '40')])
        print(len(patient_ids))

    def action_open_appointments(self):
        # action = self.env['ir.actions.actions']._for_xml_id('bista_hms.hms_appointment_form_action')
        # if self.appointment_count > 1:
        #     action['domain'] = [('patient_id', '=', self.id)]
        # elif self.appointment_count == 1:
        #     form_view = [(self.env.ref('bista_hms.hms_appointment_form_view').id, 'form')]
        #     if 'views' in action:
        #         action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
        #     else:
        #         action['views'] = form_view
        # else:
        #     action = {'type': 'ir.actions.act_window_close'}
        #
        # action['context'] = {'default_patient_id': self.id}
        # return action

        form_view_id = self.env.ref('hms.appointment_details_form_view').id
        list_view_id = self.env.ref('hms.appointment_details_list_view').id

        res = {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'appointment.details',
            'target': 'current',
            'view_id': form_view_id,
            'context': {'default_patient_id': self.id}
        }

        if self.appointment_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('patient_id', '=', self.id)]
            res['view_id'] = False

        return res

    def action_open_prescriptions(self):
        form_view_id = self.env.ref('hms.prescription_details_form_view').id
        list_view_id = self.env.ref('hms.prescription_details_list_view').id

        res = {
            'name': 'Prescriptions',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'prescription.details',
            'target': 'current',
            'view_id': form_view_id,
            'context': {'default_patient_id': self.id}
        }

        if self.prescription_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('patient_id', '=', self.id)]
            res['view_id'] = False

        return res

    @api.model
    def write(self, vals):
        updated_record = {}
        for rec in self:
            if rec.partner_id:
                if 'name' in vals:
                    updated_record.update({'name': vals['name']})
                if 'contact_no' in vals:
                    updated_record.update({'mobile': vals['contact_no']})
                if 'email' in vals:
                    updated_record.update({'email': vals['email']})
                rec.partner_id.write(updated_record)

        res = super(PatientDetails, self).write(vals)
        return res







