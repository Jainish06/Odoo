# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SubjectSubject(models.Model):
    _name = 'subject.subject'
    _description = 'Subject Details'

    name = fields.Char(string='Subject Name', required=True)