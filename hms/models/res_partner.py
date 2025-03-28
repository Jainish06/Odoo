from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    class ResPartner(models.Model):
        _inherit = 'res.partner'


    def write(self, vals):
        if self.env.context.get('prevent_recursion'):
            return super(ResPartner, self).write(vals)
        for rec in self:
            patient_records = self.env['patient.details'].search([('partner_id', '=', rec.id)])
            updated_record = {}
            if patient_records.partner_id:
                if 'name' in vals:
                    updated_record.update({'name': vals['name']})
                if 'mobile' in vals:
                    updated_record.update({'contact_no': vals['mobile']})
                if 'email' in vals:
                    updated_record.update({'email': vals['email']})
                patient_records.with_context(prevent_recursion = True).write(updated_record)

            res = super(ResPartner, self).write(vals)
            return res

