# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class PharmacyMaster(models.Model):
    _name = 'pharmacy.master'
    _description = 'Pharmacy Master Menu'

    name = fields.Char(string='Name')

    @api.constrains('name')
    def check_duplicate_name(self):
        for rec in self:
            if rec.name:
                duplicate_names = self.env['pharmacy.master'].search_count([('name', '=', rec.name)])
                if duplicate_names > 1:
                    raise UserError('Name already exists')
