from odoo import models, fields, api
from odoo.exceptions import UserError


class RmaLineWizard(models.TransientModel):
    _name = 'rma.line.wizard'

    return_line_ids = fields.One2many('return.lines', 'rma_wizard_line_id', string='Return Lines')
    ticket_id = fields.Many2one('sale.rma', string='Ticket')

    # def default_get(self, fields_list):
    #     res = super(RmaLineWizard, self).default_get(fields_list)
    #     res['ticket_id'] = self.env.context.get('active_id')
    #     return res

    @api.onchange('ticket_id')
    def get_return_lines(self):
        list = []
        self.ticket_id = self.env.context.get('active_id')
        if self.ticket_id.id:
            rma_lines = self.env['sale.rma'].browse(self.ticket_id.id)
            for lines in rma_lines.rma_line_ids:
                list.append((0,0, {
                    'product_id' : lines.product_id.id,
                    'qty_avail' : lines.qty_avail,
                    'sale_rma_line_id' : lines.id,
                    # 'return_qty' : lines.qty,
                }))
        self.return_line_ids = list

    def prepare_picking_values(self):
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
        self.ticket_id = self.env.context.get('active_id')
        values = {
            'partner_id': self.ticket_id.sale_order_id.partner_id.id,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': picking_type.default_location_dest_id.id,
            'picking_type_id': picking_type.id,
            'origin' : self.ticket_id.name,
            'sale_rma_id': self.ticket_id.id,
        }
        return values

    def prepare_picking_line_vals(self, stock_picking_id):
        line_vals_list = []
        for line in self.return_line_ids:
            line_vals = {
                'product_id': line.product_id.id,
                'product_uom_qty': line.return_qty,
                'picking_id': stock_picking_id.id,
                'location_id': stock_picking_id.location_id.id,
                'location_dest_id': stock_picking_id.location_dest_id.id,
                'name': line.product_id.display_name,
                'sale_rma_line_move_id': line.sale_rma_line_id.id,
            }
            line_vals_list.append(line_vals)
        return line_vals_list

    def action_create_return(self):
        vals = self.prepare_picking_values()

        stock_picking_id = self.env['stock.picking'].create(vals)

        line_vals_list = self.prepare_picking_line_vals(stock_picking_id)

        line_ids = self.env['stock.move'].create(line_vals_list)

        if not line_ids:
            stock_picking_id.unlink()
            raise UserError('Add Product!')


class ReturnLines(models.TransientModel):
    _name = 'return.lines'

    rma_wizard_line_id = fields.Many2one('rma.line.wizard', 'Rma wizard Line')
    product_id = fields.Many2one('product.product', 'Product')
    qty = fields.Integer(string='Quantity')
    qty_avail = fields.Integer(string='Avail Quantity')
    return_qty = fields.Integer(string='Return qty')
    sale_rma_line_id = fields.Many2one('sale.rma.line', 'RMA Lines')




