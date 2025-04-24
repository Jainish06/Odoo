from odoo import api, fields, models

class DocumentLine(models.Model):
    _name = 'document.line'
    _description = 'Document Lines'

    doc_id = fields.Many2one('documents.custom', 'Document')
    product_ids = fields.Many2many('product.template', string='Product IDs')
    sale_order_doc_id = fields.Many2one('sale.order', 'Sale Order')