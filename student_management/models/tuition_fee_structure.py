# -*- coding: utf-8 -*-
from odoo import models, fields, api

STANDARD = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('6', '6'), ('7', '7'), ('8', '8'),('9', '9'),('10', '10'), ('11', '11'), ('12', '12')]


class TuitionFeeStructure(models.Model):
    _name = 'tuition.fee.structure'
    _description = 'Tuition Fee Structure'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.template', string='Products', domain=[('type', '=', 'service')])
    fee_amount = fields.Float(string='Fee Amount')
    quantity = fields.Float(string='Quantity')
    discount = fields.Float(string='Discount')
    subtotal = fields.Float(compute='_compute_sub_total',string='Subtotal')
    total = fields.Float(compute='_compute_total',string='Total')
    standard = fields.Selection(STANDARD, string='Standard')

    '''Computes subtotal without discount'''
    @api.depends('fee_amount', 'quantity')
    def _compute_sub_total(self):
        for rec in self:
            rec.subtotal = rec.fee_amount * rec.quantity

    '''Computes total with discount'''
    @api.depends('subtotal', 'discount')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.subtotal - ((rec.subtotal * rec.discount)/100)

    '''Brings product price to fee amount'''
    @api.onchange('product_id')
    def onchange_product(self):
        self.fee_amount = self.product_id.list_price