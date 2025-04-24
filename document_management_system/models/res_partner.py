from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    tag_ids = fields.Many2many('doc.tag.master', string='Doc Tags')