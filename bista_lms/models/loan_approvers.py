from odoo import api, fields, models

class LoanApprovers(models.Model):
    _name = 'loan.approvers'
    _description = 'Levels of loan approvers'

    name = fields.Char(string='Name')
    level = fields.Integer(compute='_compute_new_level', string='Level')
    user_ids = fields.Many2many('res.users', string='User')
    loan_approver_team_id = fields.Many2one('loan.approver.team', string='Loan Approver Team')

    @api.depends('loan_approver_team_id.loan_approvers_ids')
    def _compute_new_level(self):
        for rec in self:
            tmp_level = 0
            for level in rec.loan_approver_team_id.loan_approvers_ids:
                tmp_level += 1
                level.level = tmp_level