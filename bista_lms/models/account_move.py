from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    loan_id = fields.Many2one('loan.details', string='Loan Num')
