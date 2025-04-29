# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleRma(models.Model):
    _name = 'sale.rma'
    _description = 'Return Management'

    name = fields.Char(string="Team ID", copy=False, readonly=True, index=True, default="New")
    team_id = fields.Many2one('teams', string='Team name')
    date = fields.Date(string='Date')
    sale_order_id = fields.Many2one('sale.order', 'Sale Order')
    rma_line_ids = fields.One2many('sale.rma.line', 'sale_rma_id', string='RMA Lines')
    picking_ids = fields.One2many('stock.picking', 'sale_rma_id', 'Picking')
    picking_count = fields.Integer(compute='_compute_picking_count', string='Picking Count', store=True)
    move_ids = fields.One2many('account.move', 'sale_rma_id', string='Invoice')
    invoice_count = fields.Integer(compute='_compute_invoice_count', string='Invoice Count', store=True)
    display_name = fields.Char(compute='_compute_display_name', string='Name')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            t_id = self.env['teams'].browse(vals['team_id'])
            team_code = self.env['ir.sequence'].next_by_code(t_id.code)
            vals.update({'name' : team_code})
        return super(SaleRma, self).create(vals_list)

    @api.onchange('sale_order_id')
    def get_lines(self):
        for rec in self:
            rec.rma_line_ids = [(5,0,0)]
            list = []
            for lines in rec.sale_order_id.order_line:
                list.append((0,0,{
                    'product_id' : lines.product_id.id,
                    'qty' : lines.product_uom_qty,
                    'unit_price' : lines.price_unit,
                }))
            rec.rma_line_ids = list

    def action_open_return_wizard(self):
        view_id = self.env.ref('rma.rma_line_wizard_wizard').id
        print("view_id", view_id)
        return {
            'name': 'Return',
            'view_mode': 'form',
            'res_model': 'rma.line.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def action_open_invoice_wizard(self):
        view_id = self.env.ref('rma.rma_invoice_wizard_wizard').id
        print("view_id", view_id)
        return {
            'name': 'Invoice',
            'view_mode': 'form',
            'res_model': 'rma.invoice.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.depends('picking_ids.sale_rma_id')
    def _compute_picking_count(self):
        for rec in self:
            rec.picking_count = self.env['stock.picking'].search_count([('sale_rma_id', '=', rec.id)])

    @api.depends('move_ids.sale_rma_id')
    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = self.env['account.move'].search_count([('sale_rma_id', '=', rec.id)])

    def action_open_delivery_form(self):
        form_view_id = self.env.ref('stock.view_picking_form').id
        list_view_id = self.env.ref('stock.vpicktree').id

        res = {
            'name': 'Picking',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'view_id': form_view_id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        # picking_ids = self.rma_line_ids.mapped('move_ids').mapped('picking_id')
        if self.picking_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = ([('sale_rma_id', '=', self.id)])
            res['view_id'] = False

        return res

    def action_open_invoice_form(self):
        form_view_id = self.env.ref('account.view_move_form').id
        list_view_id = self.env.ref('account.view_invoice_tree').id

        res = {
            'name': 'Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': form_view_id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        # picking_ids = self.rma_line_ids.mapped('move_ids').mapped('picking_id')
        if self.invoice_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = ([('sale_rma_id', '=', self.id)])
            res['view_id'] = False

        return res

    @api.depends('team_id', 'name')
    def _compute_display_name(self):
        for rec in self:
            if self._context.get('show_name'):
                rec.display_name = rec.name
            else:
                if rec.sale_order_id:
                    rec.display_name = f"[{rec.sale_order_id.id}] {rec.name}"
                else:
                    rec.display_name = rec.name