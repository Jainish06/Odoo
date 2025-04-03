
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PrescriptionLine(models.Model):
    _name = 'prescription.line'
    _description = 'Prescription Line'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', 'Products')
    qty = fields.Integer('Quantity', default=1)
    price_unit = fields.Float('Price Unit')
    total_price = fields.Float(compute='_compute_total_price', string="Total Price")
    prescription_id = fields.Many2one('prescription.details', 'Prescription')
    delivery_line_ids = fields.One2many('stock.move', 'prescription_line_id', 'Delivery Line')
    delivered_qty = fields.Integer(compute='_compute_delivered_qty', string='Delivered Qty', store=True)

    @api.depends('price_unit', 'qty')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.price_unit * record.qty

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.lst_price

    @api.constrains('qty')
    def _check_quantity(self):
        for line in self:
            if line.qty < line.prescription_id.delivered_qty:
                raise ValidationError('Quantity cannot be less than delivered quantity.')

    @api.depends('delivery_line_ids.state')
    def _compute_delivered_qty(self):
        for record in self:
            record.delivered_qty = sum(record.delivery_line_ids.mapped(lambda r : r.quantity if r.state == 'done' else 0))