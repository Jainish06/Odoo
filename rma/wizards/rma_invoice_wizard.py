from odoo import models, fields, api

class RmaInvoiceWizard(models.TransientModel):
    _name = 'rma.invoice.wizard'
    _description = 'RMA Invoicing'

    invoice_line_ids = fields.One2many('invoice.line', 'invoice_wizard_line_id', string='Invoice Lines')
    ticket_id = fields.Many2one('sale.rma', string='Ticket')

    @api.onchange('ticket_id')
    def get_return_lines(self):
        list = []
        self.ticket_id = self.env.context.get('active_id')
        if self.ticket_id.id:
            invoice_lines = self.env['sale.rma'].browse(self.ticket_id.id)
            for line in invoice_lines.rma_line_ids:
                list.append((0, 0, {
                    'product_id': line.product_id.id,
                    'qty_avail': line.qty_to_invoice,
                    'invoice_wizard_line_id': line.id,
                    # 'return_qty' : lines.qty,
                }))
        self.invoice_line_ids = list

    def action_create_invoice(self):
        vals = self.prepare_invoice_values()

        invoice_id = self.env['account.move'].create(vals)
        print(invoice_id)
        line_vals_list = self.prepare_invoice_line_vals(invoice_id)

        line_ids = self.env['account.move.line'].create(line_vals_list)

        # self.invoice_ids = [(0, 0, [invoice_id.id])]

    def prepare_invoice_values(self):
        self.ticket_id = self.env.context.get('active_id')
        values = {
            'move_type': 'in_invoice',
            'partner_id': self.ticket_id.sale_order_id.partner_id.id,
            'partner_shipping_id': self.ticket_id.sale_order_id.partner_id.id,
            'company_id': self.env.user.company_id.id,
            'user_id': self.env.user.id,
            'invoice_date' : self.ticket_id.date,
            'sale_rma_id': self.ticket_id.id,
        }
        return values

    def prepare_invoice_line_vals(self, invoice_id):
        line_vals_list = []

        for line in self.invoice_line_ids:
            line_vals = {
                'product_id': line.product_id.id,
                'quantity': line.to_invoice_qty,
                'move_id': invoice_id.id,
            }
            line_vals_list.append(line_vals)
            # line_vals_list.append((0, 0, line_vals))
        return line_vals_list


class InvoiceLines(models.TransientModel):
    _name = 'invoice.line'

    invoice_wizard_line_id = fields.Many2one('rma.invoice.wizard', string='Invoice Wizard')
    product_id = fields.Many2one('product.product', 'Product')
    qty_avail = fields.Integer(string='Avail Quantity')
    to_invoice_qty = fields.Integer(string='Invoice Qty')