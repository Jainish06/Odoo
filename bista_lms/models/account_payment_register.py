from odoo import fields,models,api
from datetime import date
from odoo.exceptions import ValidationError

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'


    def action_create_payments(self):
        today = date.today()
        res = super().action_create_payments()
        active_id = self._context.get('active_id')
        invoice = self.env['account.move'].search([('id','=',active_id)])
        if invoice.invoice_line_ids.price_unit == self.amount:
            emi_line = invoice.loan_id.emi_line_ids.filtered(lambda record:record.date_paid == today)
            emi_line.state = 'invoice_paid'
        else:
            raise ValidationError('EMI amount cannot be changed.')
        return res