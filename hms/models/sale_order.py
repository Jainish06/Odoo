from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.details', 'Projects')
    total_amt = fields.Char(string='Total')
    discount_amt = fields.Float(string='Discount')
    lead_reference = fields.Char(string="Lead Reference")

    def _prepare_invoice(self):
        vals = super(SaleOrder, self)._prepare_invoice()
        vals['lead_referral'] = self.lead_reference
        return vals

    @api.depends('order_line.price_subtotal', 'currency_id', 'company_id', 'discount_amt')
    def _compute_amounts(self):
        res = super(SaleOrder, self)._compute_amounts()
        for order in self:
            order.total_amt = order.amount_untaxed - order.discount_amt
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    original_unit_price = fields.Float(compute='_compute_store_original_unit_price', string='Original Unit Price', store=True)

    @api.depends('product_id', 'product_uom', 'product_uom_qty', 'order_id.partner_id')
    def _compute_discount(self):
        res = super(SaleOrderLine, self)._compute_discount()
        for rec in self:
            rec.discount = rec.discount + rec.order_id.partner_id.extra_discount
        return res

    @api.depends('product_template_id')
    def _compute_store_original_unit_price(self):
        for rec in self:
            rec.original_unit_price = rec.product_id.lst_price