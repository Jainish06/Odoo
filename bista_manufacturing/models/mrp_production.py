from odoo import api, fields, models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_open_replace_wizard(self):
        view_id = self.env.ref('bista_manufacturing.mrp_replace_wizard_form_view').id
        return {
            'name': 'Replace Product',
            'view_mode': 'form',
            'res_model': 'mrp.replace.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }