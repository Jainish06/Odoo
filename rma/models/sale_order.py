from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.model
    def name_search(self, name='', args=None, operator='', limit=100):
        args = list(args or [])
        rma_partner_id = self._context.get('rma_partner_id')
        if rma_partner_id:
            domain = [('partner_id', '=', rma_partner_id)]
            # if args:
            #     domain = ['&'] + args + domain
            partners = self.search_fetch(domain, ['name'], limit=limit)
            return [(partner.id, partner.name) for partner in partners.sudo()]
        partners = self.search_fetch(args, ['name'], limit=limit)
        return [(partner.id, partner.name) for partner in partners.sudo()]

    @api.model
    def web_search_read(self, domain, specification, offset=0, limit=None, order=None, count_limit=None):
        rma_partner_id = self._context.get('rma_partner_id')
        if rma_partner_id:
            domain = ([('partner_id', '=', rma_partner_id)])
        return super().web_search_read(domain, specification, offset=offset, limit=limit, count_limit=count_limit)

