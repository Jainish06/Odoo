from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_rma_id = fields.Many2one('sale.rma', 'Sale RMA')