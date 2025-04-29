from odoo import api, fields, models

class StudentActivity(models.Model):
    _name = 'student.activity'

    name = fields.Char('Name')