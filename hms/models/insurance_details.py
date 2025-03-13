from odoo import fields, models

class InsuranceDetails(models.Model):
    _name = 'insurance.details'
    _description = 'Insurance Details'

    name = fields.Char('Insurance company name', required = True)
    insurance_company_contact = fields.Char('Insurance company contact', required = True)
    holder_ids = fields.One2many('patient.details', 'insurance_id')
