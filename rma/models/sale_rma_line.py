# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleRmaLine(models.Model):
    _name = 'sale.rma.line'
    _description = 'Return Management'

    # name = fields.Char(string='Sale Order')
    # product = fields.Char(string='Product')
    # qty = fields.Integer(string='Quantity')
    # unit_price = fields.Integer(string='Unit Price')
    sale_order_id = fields.Many2one('sale.order', 'Sale Order')
    sale_rma_id = fields.Many2one('sale.rma')




