from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    sale_rma_line_move_id = fields.Many2one('sale.rma.line', 'RMA Lines')