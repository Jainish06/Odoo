from odoo import models, fields, api


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_approval = fields.Boolean("Sale Order Approval", config_parameter='practical_jainishpathak.sale_approval')

    sale_min_amount = fields.Float(string="Minimum Amount", readonly=False, config_parameter='practical_jainishpathak.sale_min_amount')


    # @api.onchange('sale_approval', 'sale_min_amount')
    # def onchange_sale_aproval(self):
    #     self.env['ir.config_parameter'].set_param('practical_jainishpathak.sale_approval', self.sale_approval)
    #     self.env['ir.config_parameter'].set_param('practical_jainishpathak.sale_min_amount', self.sale_min_amount)

