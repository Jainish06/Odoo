import base64
import io

import xlsxwriter

from odoo import api, fields, models
import xlwt
import pandas as pd


class MrpReportWizard(models.TransientModel):
    _name = 'mrp.report.wizard'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    mo_id = fields.Many2one('mrp.production', string='Manufacturing Order')

    def mrp_report_excel(self):
        records = self.env['mrp.production'].search(
            [('date_start', '>', self.start_date),
             ('date_start', '<', self.end_date)])
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Sheet 1')
        for rec in records:
            names = []
            data = {'Name': rec.name}
            names.append(data)
        row = 0
        col = 0
        for dict in names:
            for key, val in (dict.items()):
                worksheet.write(row, col, key)
                worksheet.write(row, col + 1, val)
                row += 1
        workbook.close()
        output.seek(0)

        file_data = base64.b64encode(output.read())
        file_name = 'demoReport.xlsx'
        attachment = self.env['ir.attachment'].create({
            'name': file_name,
            'type': 'binary',
            'datas': file_data,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }

    def button_print_xl_report(self):
        self.mrp_report_excel()
