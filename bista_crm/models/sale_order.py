from datetime import date

from odoo import models, fields, api
from odoo.api import ValuesType, Self
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    probability_stage_id = fields.Many2one('crm.probability.stage', 'Probability Stage', related='opportunity_id.probability_stage_id', readonly=False)


    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if not self.probability_stage_id and self.opportunity_id:
            records = self.env['crm.probability.stage'].search([('percentage', '=', 100.00)])
            if records:
                for rec in records:
                    self.probability_stage_id = rec.id
            else:
                raise ValidationError('No required stage for confirmation.')
        return res



    def action_process_all(self):
        self.action_confirm()
        for order in self:
            for line in order.order_line:
                for move in line.move_ids:
                    if move.state not in ['done', 'cancel']:
                        move.quantity = line.process_qty

        purchase_order_ids = self._get_purchase_orders()
        if purchase_order_ids:
            for po in purchase_order_ids:
                po.button_confirm()
                for line in po.order_line:
                    for move in line.move_ids:
                        for so_line in self.order_line:
                            if move.product_id.id == so_line.product_id.id:
                                move.quantity = so_line.process_qty
                                break
                resDict = po.picking_ids.button_validate()
                pickings_to_validate = resDict['context'].get('button_validate_picking_ids')
                pickings_to_validate = self.env['stock.picking'].browse(pickings_to_validate).with_context(skip_backorder=True)
                po.action_view_picking()
                pickings_to_validate.button_validate()
                po.action_create_invoice()
                po.invoice_ids.update({'invoice_date' : date.today()})
                po.invoice_ids.action_post()
                get_active_ids = po.invoice_ids.action_register_payment()
                self.env['account.payment.register'].with_context(get_active_ids['context']).create({})._create_payments()
        resDict = self.picking_ids.button_validate()
        pickings_to_validate = resDict['context'].get('button_validate_picking_ids')
        pickings_to_validate = self.env['stock.picking'].browse(pickings_to_validate).with_context(skip_backorder=True)
        pickings_to_validate.button_validate()
        if pickings_to_validate.state == 'done':
            self._create_invoices()
            self.invoice_ids.action_post()
            get_active_ids = self.invoice_ids.action_register_payment()
            self.env['account.payment.register'].with_context(get_active_ids['context']).create({})._create_payments()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    process_qty = fields.Integer(string='Process Qty')

    # def onchange():(self, values):
    #     if self.process_qty:
    #         values['product_uom_qty'] = self.process_qty
    #     res = super(SaleOrderLine, self).write({})
    #     return

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        self.move_ids.quantity = self.process_qty
        return res


# class StockMove(models.Model):
#     _inherit = 'stock.move'
#
#     @api.model_create_multi
#     def create(self, vals):
#         res = super(StockMove, self).write(vals)
#         self.quantity = self.sale_line_id.process_qty
#         return res