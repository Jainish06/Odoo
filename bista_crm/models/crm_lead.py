# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CrmLead(models.Model):
   _inherit = 'crm.lead'

   product_ids = fields.Many2many('product.product', string='Products')
   probability_stage_id = fields.Many2one('crm.probability.stage', 'Probability Stage')

   # def _prepare_opportunity_quotation_context(self):
   #    """ Prepares the context for a new quotation (sale.order) by sharing the values of common fields """
   #    res = super(CrmLead, self)._prepare_opportunity_quotation_context()
   #    self.ensure_one()
   #    products = []
   #    for product in self.product_ids:
   #       products.append(product.id)
   #    res.update({'default_order_line' : products})
   #    return res

   def _prepare_opportunity_quotation_context(self):
      """ Prepares the context for a new quotation (sale.order) by sharing the values of common fields """
      res = super(CrmLead, self)._prepare_opportunity_quotation_context()
      self.ensure_one()
      order_lines = []
      for product in self.product_ids:
         order_lines.append((0, 0, {'product_id': product.id, }))
      res.update({'default_order_line': order_lines})
      return res