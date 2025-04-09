from odoo import models, fields, api


class QuantityUpdateWizard(models.TransientModel):
    _name = 'qty.update.wizard'
    _inherit = 'stock.quant'
    _description = 'Quantity update on location'

    qty_location_id = fields.Many2one('stock.location', 'Location')
    qty_update = fields.Float(string='Quantity')
    # product_tmpl_id = fields.Many2one('product.template')

    # @api.depends('quantity', 'qty_update')
    # def _compute_inventory_quantity_auto_apply(self):
    #     for rec in self:
    #         rec.inventory_quantity_auto_apply = rec.with_context(location_id = rec.qty_location_id.id).qty_update

    def action_update_qty(self):

        records = self.env['stock.quant'].search([('location_id', '=', self.qty_location_id)])
        for rec in records:
            rec.inventory_quantity_auto_apply = rec.qty_update