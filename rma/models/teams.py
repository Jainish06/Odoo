# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Teams(models.Model):
    _name = 'teams'
    _description = 'Teams'

    name = fields.Char(string='Team name')
    prefix = fields.Char(string='Prefix for team')
    code = fields.Char(string='Team code')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['code'] = f'teams.{vals['name']}'
            self.env['ir.sequence'].create({
                'name': f'Sale RMA {vals['name']}',
                'code': f'teams.{vals['name']}',
                'prefix': f'{vals['prefix']}',
                'padding': 4,
            })
        return super(Teams, self).create(vals_list)




