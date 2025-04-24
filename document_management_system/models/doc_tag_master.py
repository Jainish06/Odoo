from odoo import models, fields, api


class DocTagMaster(models.Model):
    _name = 'doc.tag.master'
    _description = 'Tag master'

    name = fields.Char(string='Tag Name')