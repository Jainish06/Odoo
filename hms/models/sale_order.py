from num2words import num2words
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.details', 'Projects')
    total_amt = fields.Char(compute='_compute_amounts', string='Total')
    discount_amt = fields.Float(string='Discount')
    lead_reference = fields.Char(string="Lead Reference")
    amount_in_words = fields.Char(compute='_compute_amounts', string='Amount in Words')

    def _prepare_invoice(self):
        vals = super(SaleOrder, self)._prepare_invoice()
        if self.lead_reference:
            vals['lead_reference'] = self.lead_reference
        return vals

    @api.depends('order_line.price_subtotal', 'currency_id', 'company_id', 'discount_amt', 'amount_total')
    def _compute_amounts(self):
        res = super(SaleOrder, self)._compute_amounts()
        for order in self:
            order.total_amt = order.amount_untaxed - order.discount_amt
            order.amount_in_words = num2words(order.amount_total, lang='en_IN', to='currency').title()
        return res


class SaleOrderLine(models.Model):
    _inherit = ['sale.order.line']

    original_unit_price = fields.Float(compute='_compute_store_original_unit_price', string='Original Unit Price', store=True)
    wh_avail_qty = fields.Integer(compute='_compute_quantities', string='WH Avail Qty')
    wh_location_ids = fields.Many2many('stock.location', string='Locations')
    avail_qty_loc = fields.Integer(compute='_compute_quantities', string='Loc Avail Qty')


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

    # @api.depends('order_id.warehouse_id')
    def _compute_quantities(self):
        for rec in self:
            rec.wh_avail_qty = rec.product_id.with_context(warehouse_id = rec.order_id.warehouse_id.id).qty_available
            rec.avail_qty_loc = rec.product_id.with_context(location_id = rec.wh_location_ids.ids).qty_available