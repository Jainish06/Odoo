# -*- coding: utf-8 -*-
from black.nodes import first_leaf

from odoo import models, fields, api


class SaleRma(models.Model):
    _name = 'sale.rma'
    _description = 'Return Management'

    name = fields.Char(string="Team ID", copy=False, readonly=True, index=True, default="New")
    team_id = fields.Many2one('teams', string='Team name')
    date = fields.Date(string='Date')
    sale_order_id = fields.Many2one('sale.order', 'Sale Order')
    rma_line_ids = fields.One2many('sale.rma.line', 'sale_rma_id', string='RMA Lines')

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if rec['team_id']:
                team = self.env['teams'].browse(rec['team_id'])
                prefix = team.prefix
                seq_name = f'Sale RMA {team.name}'
                seq_code = f'sale.rma.{team.id}'

                if not self.env['ir.sequence'].search([('code', '=', seq_code)], limit=1):
                    self.env['ir.sequence'].create({
                        'name': seq_name,
                        'code': seq_code,
                        'prefix': prefix,
                        'padding': 4,
                    })
                rec['name'] = self.env['ir.sequence'].next_by_code(seq_code)
            return super(SaleRma, self).create(vals)


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
                    'to_receive_qty' : lines.product_uom_qty,
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