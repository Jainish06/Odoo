from odoo import api, fields, models

class AddProductWizard(models.TransientModel):
    _name = 'add.product.wizard'

    product_ids = fields.Many2many('product.product', string='Products')
    so_id = fields.Many2one('sale.order', string='Ticket')

    def button_add_products_from_wizard(self):
        list = []
        self.so_id = self.env.context.get('active_id')
        if self.so_id.id:
            # records = self.env['sale.order'].browse(self.ticket_id.id)
            for product in self.product_ids:
                list.append((0, 0, {
                    'product_id': product.id,
                    # 'name' : product.name,
                    'product_uom_qty' : 1
                }))
        self.so_id.order_line = list

