from odoo import api, fields, models


class LoanApproverDetails(models.Model):
    _name = 'loan.approver.details'
    _description = 'Levels of loan approvers'

    state_selection = [('pending', 'Pending'),
                       ('to_approve', 'To Approve'),
                       ('approved', 'Approved'), ('rejected', 'Rejected')]

    name = fields.Char(string='Name')
    level = fields.Integer(string='Level')
    user_ids = fields.Many2many('res.users', string='User')
    state = fields.Selection(state_selection, string='State')
    approved_by_id = fields.Many2one('res.users', string='Approved By')
    rejected_by_id = fields.Many2one('res.users', string='Rejected By')
    time_stamp = fields.Datetime(string='Time Stamp')
    loan_details_id = fields.Many2one('loan.details', string='Loan Details')

