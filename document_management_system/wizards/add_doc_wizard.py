from odoo import api, fields, models

class AddDocWizard(models.TransientModel):
    _name = 'add.doc.wizard'

    product_ids = fields.Many2many('product.template', string='Products')
    ticket_id = fields.Many2one('sale.order', string='Ticket')

    def button_add_products_from_wizard(self):
        list = []
        self.ticket_id = self.env.context.get('active_id')
        if self.ticket_id.id:
            records = self.env['sale.order'].browse(self.ticket_id.id)
            for product in self.product_ids:
                list.append((0, 0, {
                    'product_template_id': product.id,
                    'name' : product.name,
                }))
        records.order_line = list

# class AddDocWizardLine(models.TransientModel):
