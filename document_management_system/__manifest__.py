# -*- coding: utf-8 -*-
{
    'name': "DMS",

    'description': """
Long description of module's purpose
    """,

    'author': "Jainish Pathak",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'product', 'sale', 'stock'],

    'data': [
        'security/ir.model.access.csv',
        'data/system_param.xml',
        'data/email_tamplate.xml',
        'views/documents_custom.xml',
        'views/doc_tag_master.xml',
        'views/res_partner.xml',
        'views/product_template.xml',
        'wizards/add_doc_wizard.xml',
        'views/sale_order.xml',
        'views/stock_picking.xml',
        'views/do_report_inherit_template.xml',
        'views/document_line.xml',
        'views/so_report_inherit.xml'

    ],
    'application' : True,
}

