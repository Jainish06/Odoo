# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PreviousYearMarks(models.Model):
    _name = 'previous.year.marks'
    _description = 'Previous year marks of students.'
    _rec_name = 'subject'

    subject = fields.Many2one('subject.subject', 'Subject', required=True)
    total_marks = fields.Float(string='Total Marks', required=True)
    obtained_marks_exam = fields.Float(string='Obtained marks in exam.', required=True)
    obtained_marks_viva = fields.Float(string='Obtained marks in viva.', required=True)
    # Computed field from obtained_marks_exam and obtained_marks_viva.
    total_obtained_marks = fields.Float(compute='_compute_total_marks', string='Total obtained marks.')
    student_id = fields.Many2one('res.student', 'Student')

    '''Computes total marks.'''
    @api.depends('obtained_marks_exam', 'obtained_marks_viva')
    def _compute_total_marks(self):
        for rec in self:
            if rec.obtained_marks_exam:
                rec.total_obtained_marks = rec.obtained_marks_exam + rec.obtained_marks_viva
