from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AddNumWizard(models.TransientModel):
    _name = 'add.num.wizard'

    num = fields.Integer(string='Number')
    mo_id = fields.Many2one('mrp.production', string='Manufacturing')
    # avail_lot_count = fields.Integer(string='Available lot size')

    def assign_lot_num(self):
        self.mo_id = self.env.context.get('active_id')
        for count in range(self.num):
            sequence = self.mo_id.product_id.sequence_id.next_by_id()
            lot_id = self.env['stock.lot'].create({
                'name' : sequence,
                'product_id' : self.mo_id.product_id.id,
            })
            self.mo_id.serial_ids = [(4, lot_id.id)]

    @api.constrains('num')
    def check_qty_for_num_of_lot(self):
        for record in self:
            record.mo_id = self.env.context.get('active_id')
            if record.num > record.mo_id.product_qty or record.num < 0:
                raise ValidationError('Invalid lot num assignment.')