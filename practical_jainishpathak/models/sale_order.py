from datetime import timedelta

from packaging.utils import _

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import format_list


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    service_product_count = fields.Integer(compute='compute_service_products', string='Service Products', store=True)
    state = fields.Selection(selection_add = [ ('to approve', 'To Approve'), ('sale',)])
    date_approve = fields.Datetime('Confirmation Date', readonly=True, index=True, copy=False)

    # sale_min_amount = fields.Float(string="Minimum Amount", readonly=False,
    #                                config_parameter='practical_jainishpathak.sale_min_amount')

    @api.depends('order_line.product_template_id')
    def compute_service_products(self):
        for rec in self:
            for product in rec.order_line:
                service_records = self.env['product.product'].search_count([('id', '=', product.id), ('type', '=', 'service')])
                rec.service_product_count = service_records

    def button_add_products(self):
        view_id = self.env.ref('practical_jainishpathak.add_product_wizard_wizard').id
        return {
            'name': 'Add Products',
            'view_mode': 'form',
            'res_model': 'add.product.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


    # def _confirmation_error_message(self):
    #     """ Return whether order can be confirmed or not if not then returm error message. """
    #     self.ensure_one()
    #     if self.state not in {'draft', 'sent', 'to approve'}:
    #         return _("Some orders are not in a state requiring confirmation.")
    #     if any(
    #             not line.display_type
    #             and not line.is_downpayment
    #             and not line.product_id
    #             for line in self.order_line
    #     ):
    #         return _("A line on these orders missing a product, you cannot confirm it.")
    #
    #     return False
    #
    # def _approval_allowed(self):
    #     """Returns whether the order qualifies to be approved by the current user"""
    #     self.ensure_one()
    #     return (self.amount_total < float(self.env['ir.config_parameter'].sudo().get_param('practical_jainishpathak.sale_min_amount')),
    #                 self.date_order or fields.Date.today()
    #         or self.env.user.has_group('practical_jainishpathak.so_approver'))
    #
    # def button_approve(self, force=False):
    #     self.with_context(approved=True)
    #     self = self.filtered(lambda order: order._approval_allowed())
    #     self.write({'state': 'sale', 'date_approve': fields.Datetime.now()})
    #     return {}
    #
    # def action_confirm(self):
    #     if self._context.get('approved'):
    #         super(SaleOrder, self).action_confirm()
    #     else:
    #         for order in self:
    #             if order._approval_allowed():
    #                 order.button_approve()
    #             else:
    #                 order.write({'state': 'to approve'})


    # def button_cancel(self):
    #     sale_orders_with_invoices = self.filtered(
    #         lambda so: any(i.state not in ('cancel', 'draft') for i in so.invoice_ids))
    #     if sale_orders_with_invoices:
    #         raise UserError(
    #             _("Unable to cancel sale order(s): %s. You must first cancel their related vendor bills.",
    #               format_list(self.env, sale_orders_with_invoices.mapped('display_name'))))
    #     self.write({'state': 'cancel', 'mail_reminder_confirmed': False})

