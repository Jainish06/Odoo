from odoo import models, api, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    lead_reference = fields.Char(string="Lead Reference")
    prescription_id = fields.Many2one('prescription.details', 'Prescriptions')