# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CrmLead(models.Model):
   _inherit = 'crm.lead'

   product_ids = fields.Many2many('product.product', string='Products')

