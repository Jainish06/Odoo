# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleRmaLine(models.Model):
    _name = 'sale.rma.line'
    _description = 'Return Management'

    product_id = fields.Many2one('product.product', string='Product')
    qty = fields.Integer(string='Quantity')
    unit_price = fields.Integer(string='Unit Price')
    qty_avail = fields.Integer(compute='_compute_avail_qty', string='Available Qty')
    to_receive_qty = fields.Integer(compute='_compute_to_receive_qty', string='Qty to receive', store=True)
    received_qty = fields.Integer(compute='_compute_received_qty', string='Qty received', store=True)
    sale_rma_id = fields.Many2one('sale.rma')
    move_ids = fields.One2many('stock.move', 'sale_rma_line_move_id', 'Moves')
    invoiced_qty = fields.Float(string='Invoiced Qty')
    qty_to_invoice = fields.Float(string='Qty to invoice')

    @api.depends('move_ids.product_uom_qty', 'move_ids.state')
    def _compute_to_receive_qty(self):
        for rec in self:
            rec.to_receive_qty = sum(rec.move_ids.filtered(lambda s: s.state != 'done' and s.state != 'cancel').mapped('product_uom_qty'))

    @api.depends('move_ids.quantity', 'move_ids.state')
    def _compute_received_qty(self):
        for rec in self:
            rec.received_qty = sum(rec.move_ids.filtered(lambda s: s.state == 'done').mapped('quantity'))

    @api.depends('to_receive_qty', 'received_qty')
    def _compute_avail_qty(self):
        for rec in self:
            if rec.to_receive_qty != 0:
                rec.qty_avail = rec.qty - rec.to_receive_qty
            else:
                rec.qty_avail = rec.qty - rec.received_qty