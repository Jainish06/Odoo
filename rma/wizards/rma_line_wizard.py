from odoo import models, fields, api


class RmaLineWizard(models.TransientModel):
    _name = 'rma.line.wizard'

    return_line_ids = fields.One2many('return.lines', 'rma_wizard_line_id', string='Return Lines')
    ticket_id = fields.Integer(string='Active Id')

    def default_get(self, fields_list):
        res = super(RmaLineWizard, self).default_get(fields_list)
        res['ticket_id'] = self.env.context.get('active_id')
        return res

    @api.onchange('ticket_id')
    def get_return_lines(self):
        self.return_line_ids = [(5,0,0)]
        list = []
        if self.ticket_id:
            rma_lines = self.env['sale.rma'].browse(self.ticket_id)
            for lines in rma_lines.rma_line_ids:
                list.append((0,0, {
                    'product_id' : lines.product_id.id,
                    'qty_avail' : lines.qty,
                }))
        self.return_line_ids = list

    def action_update_return_qty(self):
        list = []
        if self.ticket_id:
            rma_lines = self.env['sale.rma'].browse(self.ticket_id)
            for lines in rma_lines.rma_line_ids:
                list.append((1,lines.id,{
                    'to_receive_qty' : self.return_line_ids.return_qty
                }))
            rma_lines.rma_line_ids = list


class ReturnLines(models.TransientModel):
    _name = 'return.lines'

    rma_wizard_line_id = fields.Many2one('rma.line.wizard', 'Rma wizard Line')
    product_id = fields.Many2one('product.product', 'Product')
    qty_avail = fields.Integer(string='Quantity')
    return_qty = fields.Integer(string='Return qty')

