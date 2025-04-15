# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleRmaLine(models.Model):
    _name = 'sale.rma.line'
    _description = 'Return Management'

    product_id = fields.Many2one('product.product', string='Product')
    qty = fields.Integer(string='Quantity')
    unit_price = fields.Integer(string='Unit Price')
    to_receive_qty = fields.Integer(string='Qty to receive')
    received_qty = fields.Integer(string='Qty received')
    sale_rma_id = fields.Many2one('sale.rma')
    move_id = fields.Many2one('stock.move')




