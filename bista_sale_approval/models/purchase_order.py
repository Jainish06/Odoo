from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    category_id = fields.Many2one('product.category', 'Categories')