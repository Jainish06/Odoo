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

def import_product_category():
    try:
        wb = openpyxl.load_workbook('Product Categories.xlsx')
        ws = wb.active
        print(ws)
        for record in ws.iter_rows(min_row=2, max_row=None, min_col=None, max_col=None, values_only=True):
            parent_ids = []
            category_ids = []
            if record[0] and record[1]:
                category = record[0].split(' / ')[-1]
                parent = record[1].split(' / ')[-1]
                search_parent = odoo.env['product.category'].search([('name', '=', parent)])
                if not search_parent:
                    parent_id = odoo.env['product.category'].create({'name' : parent})
                search_category = odoo.env['product.category'].search([('name', '=', category)])
                if not search_category:
                    category_id = odoo.env['product.category'].create({'name' : category, 'parent_id' : parent_id[0]})

    except Exception as e:
        print(e)

import_product_category()