from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    probability_stage_id = fields.Many2one('crm.probability.stage', 'Probability Stage', related='opportunity_id.probability_stage_id', readonly=False)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if not self.probability_stage_id and self.opportunity_id:
            records = self.env['crm.probability.stage'].search([('percentage', '=', 100.00)])
            if records:
                for rec in records:
                    self.probability_stage_id = rec.id
            else:
                raise ValidationError('No required stage for confirmation.')
        return res