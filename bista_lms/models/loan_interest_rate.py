from odoo import api, fields, models

class LoanInterestRate(models.Model):
    _name = 'loan.interest.rate'
    _description = 'Interest Rates'
    _rec_name = 'loan_id'

    loan_id = fields.Many2one('loan.details', string='Loan Name')
    interest_rate = fields.Float(string='Interest Rate')
    issued_date = fields.Date(string='Interest Issue Date')
    is_active = fields.Boolean(string='Interest Active?')

    def action_activate_interest(self):
        for rec in self:
            rec.loan_id.curr_interest_rate = rec.interest_rate
            if rec.interest_rate and rec.issued_date:
                active_recs = self.env['loan.interest.rate'].search([('is_active', '=', True), ('loan_id', '=', self.loan_id.id)])
                for act in active_recs:
                    act.write({'is_active' : False})
                rec.is_active = True
