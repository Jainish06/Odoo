from odoo import fields, models

class Departments(models.Model):
    _name = 'departments'
    _description = 'Departments'

    name = fields.Char('Department name', required = True)
    doctor_ids = fields.One2many('doctor.details', 'department_id')
    staff_ids = fields.One2many('staff.details', 'department_id')
    user_ids = fields.Many2many('res.users', 'rel_user_department', 'department_ID', 'user_ID', 'User Names')
    user1_ids = fields.Many2many('res.users', 'rel_user1_department', 'user1_department_ID', 'user1_ID', 'User1 Names')

    def action_open_doctor_list_wizard(self):
        view_id = self.env.ref('hms.doctor_list_wizard_wizard').id
        print("view_id", view_id)
        return {
            'name': 'Doctors',
            'view_mode': 'form',
            'res_model': 'doctor.list.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }