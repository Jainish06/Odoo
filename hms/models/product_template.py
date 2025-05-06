from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'



    def action_update_qty1(self):
        view_id = self.env.ref('hms.quantity_update_wizard_wizard').id
        print("view_id", view_id)
        return {
            'name': 'Update Loc quantity',
            'view_mode': 'form',
            'res_model': 'qty.update.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            # 'context' : {'default_product_id' : self.id}
        }