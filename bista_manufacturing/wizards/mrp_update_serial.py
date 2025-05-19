from odoo import api, fields, models

class MrpUpdateSerial(models.TransientModel):
    _name = 'mrp.update.serial'
    _description = 'Product serial update'

    mo_num = fields.Char(string='MO Number')
    current_product_code = fields.Char(string='Current Product')
    old_product_serial = fields.Char(string='Old Product Serial')
    new_product_serial = fields.Char(string='New Product Serial')
    mrp_replace_wizard_id = fields.Many2one('mrp.replace.wizard', string='Replace Wizard')