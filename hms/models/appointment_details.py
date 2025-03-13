import datetime
from odoo import fields, models, api
from odoo.exceptions import UserError


class AppointmentDetails(models.Model):
    _name = 'appointment.details'
    _description = 'Appointment Details'

    name = fields.Char(string="Appointment ID", copy=False, readonly=True, index=True, default="New")
    patient_id = fields.Many2one('patient.details', string = 'Patient Name', required = True)
    main_complain = fields.Text('Main Complain', required = True)
    contact_no = fields.Char('Phone number', required = True)
    app_date_time = fields.Datetime('Date and time', required = True)
    doctor_appointment_id = fields.Many2one('doctor.details', 'Doctor assigned')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('waiting', 'Waiting'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')],
                             string="Status", default='draft')

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

    @api.constrains('app_date_time')
    def check_date(self):
        for record in self:
            if record.app_date_time <= fields.Datetime.now():
                raise UserError("Invalid date.")
