from odoo import models, api, fields
from odoo.api import depends


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    lead_reference = fields.Char(string="Lead Reference")
    prescription_id = fields.Many2one('prescription.details', 'Prescriptions')