from odoo import api, fields, models

class AddDocWizard(models.TransientModel):
    _name = 'add.doc.wizard'

    product_ids = fields.Many2many('product.template', string='Products')
    ticket_id = fields.Many2one('sale.order', string='Ticket')

    def button_add_products_from_wizard(self):
        list = []
        self.ticket_id = self.env.context.get('active_id')
        if self.ticket_id.id:
            # records = self.env['sale.order'].browse(self.ticket_id.id)
            for product in self.product_ids:
                list.append((0, 0, {
                    'product_id': product.product_variant_id.id,
                    'name' : product.name,
                }))
        self.ticket_id.order_line = list
        for rec in self.ticket_id:
            docs = rec.order_line.product_template_id.document_ids.filtered(lambda doc: any(tag in rec.doc_tag_ids for tag in doc.tag_ids))
            for doc in docs:
                record = self.env['document.line'].search([('doc_id', '=', doc.id), ('sale_order_doc_id', '=', rec.id)])
                if record:
                    self.env['document.line'].write({'product_ids' : [(6,0,rec.order_line.product_template_id.id)]})
                else:
                    self.env['document.line'].create({
                        'doc_id' : doc.id,
                        'product_ids' : [(6,0,rec.order_line.product_template_id.id)],
                        'sale_order_doc_id' : rec.id
                    })
# class AddDocWizardLine(models.TransientModel):
