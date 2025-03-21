from odoo import fields, models, api

class PrescriptionDetails(models.Model):
    _name = 'prescription.details'
    _description = 'Prescription Details'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('patient.details', 'Patients')
    date = fields.Date('Date')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('cancel', 'Cancel')], 'State', default='draft')
    prescription_line_ids = fields.One2many('prescription.line', 'prescription_id', 'Prescription Lines')
    total_amount = fields.Float(compute='_compute_total_amount', string='Total Amount', store=True)

    # @api.depends('prescription_line_ids.total_price')
    # def _compute_total_amount(self):
    #     for record in self:
    #         record.total_amount = sum(record.prescription_line_ids.mapped('total_price'))

    def action_confirm(self):
        self.state = 'confirm'

    def action_cancel(self):
        self.state = 'cancel'