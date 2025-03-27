# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError

STANDARD = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('6', '6'), ('7', '7'), ('8', '8'),('9', '9'),('10', '10'), ('11', '11'), ('12', '12')]


class ResStudent(models.Model):
    _name = 'res.student'
    _description = 'Student Details'

    name = fields.Char(string='Student Name', required=True)
    registration_id = fields.Char(string="Registration ID", copy=False, readonly=True, index=True, default="New")
    registration_date = fields.Date(string='Registration Date', required=True)
    birth_date = fields.Date(string='Birth Date', required=True)
    age = fields.Char(compute='_compute_age', string='Age', store=True)  #Compute field, age computed from birthdate.
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    standard = fields.Selection(STANDARD, string='Standard')
    guardian_name = fields.Char(string='Guardian Name')
    guardian_phone = fields.Char(string='Guardian Phone')
    previous_year_marks_ids = fields.One2many('previous.year.marks', 'student_id', 'Previous Year Marks')
    tuition_fee_structure_id = fields.Many2one('tuition.fee.structure', 'Tuition Fee Structure')
    is_blocked = fields.Boolean(string='Is Blocked?')
    is_expired = fields.Boolean(string='Is Expired?')

    @api.depends('registration_id')
    def _compute_display_name(self):
        for rec in self:
            if rec.registration_id != 'New':
                rec.display_name = f"[{rec.registration_id}] {rec.name}"
            else:
                rec.display_name = 'New'

    '''Unique ID generation'''
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val.update({'registration_id': self.env['ir.sequence'].next_by_code('res.student')})
        res = super(ResStudent, self).create(vals_list)
        return res

    @api.constrains('phone')
    #check length of phone
    def check_phone(self):
        for record in self:
            if record.phone and len(record.phone) < 10:
                raise UserError("Phone number should be minimum 10 digits")

            # check no duplicate phone number
            patient_ids = self.env['res.student'].search_count(
                [('phone', '=', record.phone), ('id', '!=', record.id)])
            if patient_ids:
                raise UserError("Phone number already exists")

    '''Compute age from birth date'''
    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                current_date = fields.Date.today()
                age_delta = relativedelta(current_date, rec.birth_date)
                rec.age = f"{age_delta.years} Year(s), {age_delta.months} Month(s)"

    '''Block button action to make is_block file true'''
    def action_block(self):
        self.is_blocked = True

    '''Unblock button action to make is_block file false'''
    def action_unblock(self):
        self.is_blocked = False

    '''Schedule action for checking student registration'''
    def _check_student_registration(self):
        # This method will be called by a cron job
        today = fields.Datetime.today()
        date = today - timedelta(days=30)
        expired_records = self.env['res.student'].search([('registration_date', '<', date), ('is_blocked', '=', False)])
        for rec in expired_records:
            rec.is_expired = True


