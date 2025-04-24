from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    document_ids = fields.Many2many('documents.custom', string='Documents')

