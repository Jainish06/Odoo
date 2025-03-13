from odoo import fields, models

class StaffDetails(models.Model):
    _name = 'staff.details'
    _description = 'Staff Details'

    name = fields.Char('Staff person name', required = True)
    designation = fields.Char('Designation', required = True)
    contact_no = fields.Char('Phone number', required = True)
    department_id = fields.Many2one('departments', 'Department')