from odoo import models, fields, api

class CrmProbabilityStage(models.Model):
    _name = 'crm.probability.stage'
    _description = 'Probability Stages'

    name = fields.Char(string='Name')
    percentage = fields.Float(string='Percentage')

