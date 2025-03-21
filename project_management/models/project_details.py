from datetime import timedelta, datetime

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProjectDetails(models.Model):
    _name = 'project.details'
    _description = 'Project Details'

    name = fields.Char(' Project name', required=True)
    project_code = fields.Char(string="Project ID", copy=False, readonly=True, index=True, default="New")
    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')
    duration = fields.Float(compute='_compute_total_duration', string='Total duration', store=True)
    status = fields.Selection([('draft', 'Draft'), ('in-progress', 'In Progress'), ('completed', 'Completed')], default='draft')
    team_lead_id = fields.Many2one('res.partner', 'Team Lead')
    team_members = fields.Many2many('res.partner', 'rel_team_members', 'team_project_id', 'team_member_id', 'Team Members')
    task_ids = fields.One2many('task.details', 'project_id', 'Task Id')
    task_count = fields.Integer(compute='_task_count', string='Task Count')

    @api.constrains('team_members')
    def check_members(self):
        if len(self.team_members)<2:
            raise ValidationError("Atleast 2 members required.")

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val.update({'project_code' : self.env['ir.sequence'].next_by_code('project.details')})
        res = super(ProjectDetails, self).create(vals_list)
        return res

    @api.depends('end_date')
    def _compute_total_duration(self):
        for rec in self:
            if rec.end_date:
                diff = rec.end_date - rec.start_date
                rec.duration = diff.days
                print(type(diff.days))

    def _update_state(self):
        on_going_projects = self.env['project.details'].search([('end_date', '>', datetime.now())])
        for rec in on_going_projects:
            rec.status = 'in-progress'
        overdue_projects = self.env['project.details'].search([('end_date', '<=', datetime.now())])
        for rec in overdue_projects:
            rec.status = 'completed'

    @api.depends('task_ids.project_id')
    def _task_count(self):
        for rec in self:
            rec.task_count = self.env['task.details'].search_count([('project_id', '=', rec.id)])

    def action_in_progress(self):
        self.status = 'in-progress'

    def action_completed(self):
        self.status = 'completed'

    def action_open_tasks(self):
        list_view_id = self.env.ref('project_management.task_details_list_view').id
        form_view_id = self.env.ref('project_management.task_details_form_view').id

        res = {
            'name': 'Tasks',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'task.details',
            'target': 'current',
            'view_id': form_view_id,
            'context': {'default_project_id': self.id}
        }

        if self.task_count >= 1 :
            res['view_id'] = False
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('project_id', '=', self.id)]
            res['view_mode'] = 'list,form'
        return res

    @api.constrains('name')
    def restrict_duplicate_name_per_lead(self):
        for rec in self:
            if rec.name:
                duplicates = self.env['project.details'].search([('name', '=', rec.name), ('team_lead_id', '=', rec.team_lead_id.id), ('id', '!=', rec.id)])
                if duplicates:
                    raise ValidationError("Same name cannot be assigned to same team lead.")



