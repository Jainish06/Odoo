from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    document_ids = fields.Many2many('documents.custom', string='Documents')