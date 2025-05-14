from odoo import api, fields, models

class LoanEmiLines(models.Model):
    _name = 'loan.emi.lines'
    _description = 'EMI Details'
    _rec_name = 'loan_id'

    state_selection = [('pending', 'Pending'),
                       ('invoice_generated', 'Invoice Generated'),
                       ('invoice_paid', 'EMI Paid')]

    loan_id = fields.Many2one('loan.details', string='Loan Name')
    date_paid = fields.Date(string='Date')
    total_amt = fields.Float(string='Total Amount')
    paid_interest_amt = fields.Float(string='Interest')
    paid_principle_amt = fields.Float(string='Principle')
    state = fields.Selection(state_selection, default='pending')

    # @api.depends('paid_interest_amt', 'paid_principle_amt')
    # def _compute_total_amt_paid(self):
    #     for rec in self:
    #         rec.total_amt = rec.paid_interest_amt + rec.paid_principle_amt