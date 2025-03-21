from odoo import fields, models, api
from odoo.exceptions import ValidationError


class TaskDetails(models.Model):
    _name = 'task.details'
    _description = 'Task Details'

    name = fields.Char('Task name')
    task_code = fields.Char('Task Id', copy=False, readonly=True, index=True, default="New")
    project_id = fields.Many2one('project.details', 'Project')
    assigned_to = fields.Many2one('res.partner', 'Assigned to')
    start_date = fields.Datetime('Start date')
    end_date = fields.Datetime('End date')
    task_duration = fields.Float(compute='_compute_total_duration', string='Duration', store=True)
    state = fields.Selection([('pending', 'Pending'), ('in-progress', 'In Progress'), ('completed', 'Completed')], default='pending')

    # @api.onchange('state')
    # def onchange_task_state(self):
    #     for rec in self:
    #         if rec.state:
    #             done_tasks = self.env['task.details'].search_count([('state', '=', 'completed'), ('project_id', '=', rec.project_id.id)])
    #             if done_tasks:
    #                 rec.project_id.status = 'completed'
    #             elif rec.project_id.status == 'completed':
    #                 rec.project_id.status = 'in-progress'

    @api.constrains('task_duration')
    def check_duration(self):
        for rec in self:
            if rec.project_id:
                if rec.task_duration >= rec.project_id.duration:
                    raise ValidationError('Task duration cannot more than project duration.')

    @api.depends('start_date', 'end_date')
    def _compute_total_duration(self):
        for rec in self:
            if rec.end_date:
                diff = rec.end_date - rec.start_date
                rec.task_duration = diff.days

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val.update({'task_code': self.env['ir.sequence'].next_by_code('task.details')})
        res = super(TaskDetails, self).create(vals_list)
        return res

    @api.constrains('start_date', 'end_date')
    def restrict_task_end_date(self):
        for rec in self:
            if rec.end_date:
                if rec.project_id.end_date < rec.end_date and rec.project_id.start_date > rec.start_date:
                    raise ValidationError("Task end date cannot be more than project end date")

    @api.constrains('start_date', 'end_date')
    def restrict_task_end_date(self):
        for rec in self:
            if rec.end_date:
                if rec.project_id.start_date > rec.start_date:
                    raise ValidationError("Task start date cannot be less than project start date")

    def action_in_progress(self):
        self.state = 'in-progress'

    def action_completed(self):
        self.state = 'completed'