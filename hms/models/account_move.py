from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    prescription_id = fields.Many2one('prescription.details', 'Prescriptions')