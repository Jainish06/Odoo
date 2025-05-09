from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # def button_confirm(self):
    #     res = super(PurchaseOrder, self).button_confirm()
    #     self.ensure_one()
    #     # Assuming you have some data to generate your attachment
    #
    #     mail_template = self.env.ref('practical_jainishpathak.email_template_send_vendor')
    #     if self.partner_id.email:
    #         mail_template.send_mail(self.id, force_send=False)
    #     return res