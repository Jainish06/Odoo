from odoo import models, fields, api

class RmaInvoiceWizard(models.TransientModel):
    _name = 'rma.invoice.wizard'
    _description = 'RMA Invoicing'

    invoice_line_ids = fields.One2many('invoice.line', 'invoice_wizard_line_id', string='Invoice Lines')

    def action_create_invoice(self):
        pass


class InvoiceLines(models.TransientModel):
    _name = 'invoice.line'

    invoice_wizard_line_id = fields.Many2one('rma.invoice.wizard', string='Invoice Wizard')
    product_id = fields.Many2one('product.product', 'Product')
    to_invoice_qty = fields.Integer(string='Quantity')