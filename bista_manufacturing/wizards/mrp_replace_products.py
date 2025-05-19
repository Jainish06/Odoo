from odoo import api, fields, models

class MrpReplaceProducts(models.TransientModel):
    _name = 'mrp.replace.products'
    _description = 'Products to replace from file'

    mo_num = fields.Char(string='MO Number')
    current_product_code = fields.Char(string='Current Product')
    new_product_code = fields.Char(string='New Product')
    mrp_replace_wizard_id = fields.Many2one('mrp.replace.wizard', string='Replace Wizard')