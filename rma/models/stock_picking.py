from odoo import models, api, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_rma_id = fields.Many2one('sale.rma', 'RMA')