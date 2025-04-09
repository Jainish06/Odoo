# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Teams(models.Model):
    _name = 'teams'
    _description = 'Teams'

    name = fields.Char(string='Team name')
    prefix = fields.Char(string='Prefix for team')





