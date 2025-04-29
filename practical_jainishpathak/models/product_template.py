from odoo import fields,models,api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    pharmacy_master_id = fields.Many2one('pharmacy.master', strng='Pharmacy Values')