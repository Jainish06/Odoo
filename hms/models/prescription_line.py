from email.policy import default

from odoo import fields, models, api

class PrescriptionLine(models.Model):
    _name = 'prescription.line'
    _description = 'Prescription Line'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', 'Products')
    qty = fields.Integer('Quantity', default=1)
    price_unit = fields.Float('Price Unit')
    total_price = fields.Float(compute='_compute_total_price', string="Total Price")
    prescription_id = fields.Many2one('prescription.details', 'Prescription')

    @api.depends('price_unit', 'qty')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.price_unit * record.qty

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.lst_price
