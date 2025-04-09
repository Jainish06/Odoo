from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    extra_discount = fields.Float(string='Extra Discount')
    terms_and_conditions = fields.Text(string='Terms and Conditions')
    use_customers_tc = fields.Boolean(string='Use Customers TC ?')

