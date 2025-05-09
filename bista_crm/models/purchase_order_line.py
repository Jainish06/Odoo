from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # def _prepare_picking(self):
    #     res = super(PurchaseOrder, self)._prepare_picking()
    #     if self.order_id.sale_line_id.location_id.id:
    #         res.update({'location_dest_id' : self.order_line.sale_line_id.location_id.id})
    #     return res

    def _prepare_purchase_order_line_from_procurement(self, product_id, product_qty, product_uom, location_dest_id,name, origin, company_id, values, po):
        res = super()._prepare_purchase_order_line_from_procurement(product_id, product_qty, product_uom,location_dest_id, name, origin, company_id, values,po)
        if self.order_line.sale_line_id.location_id.id:
            res.update['location_dest_id'] = self.order_line.sale_line_id.location_id.id
        return res