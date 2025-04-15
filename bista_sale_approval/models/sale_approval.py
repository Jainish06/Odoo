from odoo import models, fields, api


class SaleApproval(models.TransientModel):
    _description = 'Approval'
    _inherit = 'res.config.settings'

    so_order_approval = fields.Boolean("Sale Order Approval",
                                       default=lambda self: self.env.company.so_double_validation == 'two_step')
    so_double_validation = fields.Selection(related='company_id.so_double_validation', string="Levels of Approvals *",
                                            readonly=False)
    so_double_validation_amount = fields.Monetary(related='company_id.so_double_validation_amount',
                                                  string="Minimum Amount", currency_field='company_currency_id',
                                                  readonly=False)
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)

    def set_values(self):
        super().set_values()
        so_double_validation = 'two_step' if self.so_order_approval else 'one_step'
        if self.so_double_validation != so_double_validation:
            self.so_double_validation = so_double_validation