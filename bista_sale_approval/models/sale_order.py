from packaging.utils import _

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import format_list


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add = [ ('to approve', 'To Approve'), ('sale',)])
    date_approve = fields.Datetime('Confirmation Date', readonly=True, index=True, copy=False)

    def _confirmation_error_message(self):
        """ Return whether order can be confirmed or not if not then returm error message. """
        self.ensure_one()
        if self.state not in {'draft', 'sent', 'to approve'}:
            return _("Some orders are not in a state requiring confirmation.")
        if any(
                not line.display_type
                and not line.is_downpayment
                and not line.product_id
                for line in self.order_line
        ):
            return _("A line on these orders missing a product, you cannot confirm it.")

        return False

    def _approval_allowed(self):
        """Returns whether the order qualifies to be approved by the current user"""
        self.ensure_one()
        return (
            self.company_id.so_double_validation == 'one_step'
            or (self.company_id.so_double_validation == 'two_step'
                and self.amount_total < self.env.company.currency_id._convert(
                    self.company_id.so_double_validation_amount, self.currency_id, self.company_id,
                    self.date_order or fields.Date.today()))
            or self.env.user.has_group('sales_team.group_sale_manager'))

    def button_approve(self, force=False):
        super(SaleOrder, self).action_confirm()
        self = self.filtered(lambda order: order._approval_allowed())
        self.write({'state': 'sale', 'date_approve': fields.Datetime.now()})
        return {}

    def action_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})

    def button_cancel(self):
        sale_orders_with_invoices = self.filtered(
            lambda so: any(i.state not in ('cancel', 'draft') for i in so.invoice_ids))
        if sale_orders_with_invoices:
            raise UserError(
                _("Unable to cancel sale order(s): %s. You must first cancel their related vendor bills.",
                  format_list(self.env, sale_orders_with_invoices.mapped('display_name'))))
        self.write({'state': 'cancel', 'mail_reminder_confirmed': False})