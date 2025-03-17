from datetime import datetime, timedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Datetime
from odoo.service.server import start


class AppointmentDetails(models.Model):
    _name = 'appointment.details'
    _description = 'Appointment Details'

    name = fields.Char(string="Appointment ID", copy=False, readonly=True, index=True, default="New")
    patient_id = fields.Many2one('patient.details', string = 'Patient Name', required = True)
    main_complain = fields.Text('Main Complain', required = True)
    contact_no = fields.Char('Phone number', required = True)
    app_date_time = fields.Datetime('Date and time', required = True)
    age = fields.Char(string="Age")
    age_category = fields.Char(string="Age Category", required=True)
    guardian_type = fields.Char(string="Guardian Category", required=True)
    guardian_id = fields.Char('Guardian Id')
    doctor_appointment_id = fields.Many2one('doctor.details', 'Doctor assigned')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('waiting', 'Waiting'),
                              ('consultation_begin', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')],
                             string="Status", default='draft')
    consultation_start = fields.Datetime('Consultation start time')
    consultation_end = fields.Datetime('Consultation end time')
    total_consultation_time = fields.Float('Total consultation time')
    appointment_creation_time = fields.Datetime('Appointment creation time')
    service_product_id = fields.Many2one('product.product', 'Service Products', domain=[('type', '=', 'service')])

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val.update({'name': self.env['ir.sequence'].next_by_code('appointment.details')})
        res = super(AppointmentDetails, self).create(vals_list)
        return res

    @api.constrains('contact_no')
    def check_phone(self):
        for record in self:
            if record.contact_no and len(record.contact_no) < 10:
                raise UserError("Phone number should be minimum 10 digits")

            # check no duplicate phone number
            appointment_ids = self.env['appointment.details'].search_count(
                [('contact_no', '=', record.contact_no), ('id', '!=', record.id)])
            if appointment_ids:
                raise UserError("Phone number already exists")

    @api.constrains('app_date_time', 'patient_id')
    def check_date(self):
        for record in self:
            if record.app_date_time <= fields.Datetime.now():
                raise UserError("Invalid date.")

    @api.constrains('app_date_time', 'patient_id')
    def restrict_duplicate_appointment(self):
        for record in self:
            existing_appointment = self.env["appointment.details"].search([
                ("patient_id", "=", record.patient_id.name),
                ("app_date_time", "=", record.app_date_time),
                ("name", "!=", record.name)])
            if existing_appointment:
                raise ValidationError(
                    f"Patient {record.patient_id.name} already has an appointment on this time and date.")

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            self.contact_no = self.patient_id.contact_no

    @api.onchange('patient_id')
    def onchange_patient_id_guardian(self):
        if self.patient_id:
            self.age = self.patient_id.age
            self.age_category = self.patient_id.age_category
            self.guardian_type = self.patient_id.guardian_type
            self.guardian_id = self.patient_id.guardian_id.name
            self.appointment_creation_time = datetime.now()
    def action_confirm(self):
        self.state = 'confirm'

    def action_start(self):
        self.state = 'consultation_begin'
        self.consultation_start = Datetime.now()

    def action_done(self):
        self.state = 'done'
        self.consultation_end = Datetime.now()

    def action_cancel(self):
        self.state = 'cancel'

    @api.onchange('consultation_end')
    def onchange_time(self):
        if self.consultation_end:
            end_time = self.consultation_end.hour + self.consultation_end.minute / 60 + self.consultation_end.second / 3600
            start_time = self.consultation_start.hour + self.consultation_start.minute / 60 + self.consultation_start.second / 3600
            self.total_consultation_time = end_time - start_time

    def _auto_cancelling_overdue_app(self):
        now = datetime.now()
        cutoff_time = now - timedelta(hours=24)
        print(cutoff_time.strftime("%Y-%m-%d %H:%M:%S"))
        overdue_appointments = self.env['appointment.details'].search([('appointment_creation_time', '<=', cutoff_time.strftime("%Y-%m-%d %H:%M:%S")), ('state', '=', 'draft')])
        if overdue_appointments:
            print(overdue_appointments.state)
            for record in overdue_appointments:
                record.state = 'cancel'
                print("record--",record)
                print("State---",record.state)


    def _appointment_report(self):
        # This method will be called by a cron job
        # start_day = self.app_date_time.strftime("%A")
        appointment_ids = self.env['appointment.details'].search([('name')])
        total_appointments = len(appointment_ids)
        total_consultation_time = sum(self.env['appointment.details'].mapped("total_consultation_time"))
        patient_ids = self.env['appointment.details'].search([('patient_id'),('total_consultation_time', '>', '1')])
        patient_list = [i for i in patient_ids.patient_id.name]
        report = {'Total consultation time' : total_consultation_time, 'List of patients who consulted for more than 1 hour' : patient_list}
        print(report)

