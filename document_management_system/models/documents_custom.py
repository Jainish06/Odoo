from odoo import models, fields, api


class DocumentsCustom(models.Model):
    _name = 'documents.custom'
    _description = 'Documents'

    name = fields.Char(string='Doc Name')
    attachment_id = fields.Many2one('ir.attachment', 'Attachment')
    tag_ids = fields.Many2many('doc.tag.master', string='Tags')