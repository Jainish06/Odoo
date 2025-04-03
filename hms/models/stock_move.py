from odoo import models, api, fields
from odoo.api import depends


class StockMove(models.Model):
    _inherit = 'stock.move'

    prescription_line_id = fields.Many2one('prescription.line', 'Prescription Lines')