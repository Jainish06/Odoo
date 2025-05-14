import odoorpc
import openpyxl

# Prepare the connection to the server
odoo = odoorpc.ODOO('localhost', port=8069)

# Login
odoo.login('Evaluation', 'admin', 'admin')

# Current user
user = odoo.env.user
print(user.name)            # name of the user connected
print(user.company_id.name) # the name of its company


def import_workstations():
    try:
        wb = openpyxl.load_workbook('Work Centers.xlsx')
        ws = wb.active
        print(ws)
        for record in ws.iter_rows(min_row=2, max_row=None, min_col=None, max_col=None, values_only=True):
            tag_ids = []
            tag_list = record[1].split(',')
            if tag_list:
                for tag in tag_list:
                    search_tag = odoo.env['mrp.workcenter.tag'].search([('name', '=', tag)])
                    if search_tag:
                        tag_ids.append(search_tag[0])
                    if not search_tag:
                        tag_id = odoo.env['mrp.workcenter.tag'].create({'name' : tag})
                        if tag_id:
                            tag_ids.append(tag_id)
            alt_work_ct_ids = []
            if record[3]:
                alt_list = record[3].split(',')
                for alt in alt_list:
                    search_alt = odoo.env['mrp.workcenter'].search([('name', '=', alt.strip())])
                    if search_alt:
                        alt_work_ct_ids.append(search_alt[0])
                    if not search_alt:
                        alt_id = odoo.env['mrp.workcenter'].create({'name': record[0], 'tag_ids': [(6, 0, tag_ids)], 'code': record[2]})
                        if alt_id:
                            alt_work_ct_ids.append(alt_id)
            search_name = odoo.env['mrp.workcenter'].search([('name', '=', record[0])])
            if not search_name:
                odoo.env['mrp.workcenter'].create({'name': record[0], 'tag_ids': [(6, 0, tag_ids)], 'code': record[2], 'alternative_workcenter_ids' : [(6, 0, alt_work_ct_ids)]})
    except Exception as e:
        print(e)

import_workstations()