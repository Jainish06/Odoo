from odoo import models, fields, api

class RmaInvoiceWizard(models.TransientModel):
    _name = 'rma.invoice.wizard'
    _description = 'RMA Invoicing'

    invoice_line_ids = fields.One2many('invoice.lines', 'invoice_wizard_line_id', string='Invoice Lines')



class InvoiceLines(models.TransientModel):
    _name = 'invoice.line'

    invoice_wizard_line_id = fields.Many2one('rma.invoice.wizard', string='Invoice Wizard')