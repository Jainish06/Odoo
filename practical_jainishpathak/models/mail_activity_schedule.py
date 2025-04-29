from odoo import api, fields, models

class MailActivitySchedule(models.TransientModel):
    _inherit = 'mail.activity.schedule'

    meaningful_connection = fields.Boolean(string='Meaningful Connection')
    or_string = fields.Char(default='Or', readonly='1')
