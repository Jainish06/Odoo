from odoo import api, fields, models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    serial_ids = fields.Many2many('stock.lot', string='Serial No.')
    serial_count = fields.Integer()

    def action_open_wizard(self):
        view_id = self.env.ref('bista_crm.add_num_wizard_wizard').id
        return {
            'name': 'Add Num of Lot/Serial',
            'view_mode': 'form',
            'res_model': 'add.num.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    # def button_mark_done(self):
    #     res = super(MrpProduction ,self).button_mark_done()
    #     if self.lot_producing_id:
    #         self.serial_ids = (3,self.lot_producing_id.id)
    #     return res