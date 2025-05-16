from odoo import api, fields, models

class LoanApproverTeam(models.Model):
    _name = 'loan.approver.team'
    _description = 'Team of approvers'

    name = fields.Char(string='Team Name')
    loan_approvers_ids = fields.One2many('loan.approvers', 'loan_approver_team_id', string='Loan Approvers')