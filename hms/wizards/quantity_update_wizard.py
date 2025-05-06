from odoo import models, fields, api


class QuantityUpdateWizard(models.TransientModel):
    _name = 'qty.update.wizard'
    # _inherit = 'stock.quant'
    _description = 'Quantity update on location'

    qty_location_id = fields.Many2one('stock.location', 'Location')
    qty_update = fields.Float(string='Quantity')
    # product_tmpl_id = fields.Many2one('product.template')

    # @api.depends('quantity', 'qty_update')
    # def _compute_inventory_quantity_auto_apply(self):
    #     for rec in self:
    #         rec.inventory_quantity_auto_apply = rec.with_context(location_id = rec.qty_location_id.id).qty_update

    def action_update_quant(self):

        for rec in self:
            active_id = self.env.context.get('active_id')
            product_id = self.env['product.template'].browse(active_id)
            records = self.env['stock.quant'].search([('location_id', '=', rec.qty_location_id.id), ('product_id', '=', product_id.product_variant_id.id)])
            records.write({'inventory_quantity' : rec.qty_update})
            records._apply_inventory()
