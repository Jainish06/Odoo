from odoo import fields, models, api

class PrescriptionDetails(models.Model):
    _name = 'prescription.details'
    _description = 'Prescription Details'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('patient.details', 'Patients')
    date = fields.Date('Date')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('cancel', 'Cancel')], 'State', default='draft')
    prescription_line_ids = fields.One2many('prescription.line', 'prescription_id', 'Prescription Lines')
    total_amount = fields.Float(compute='_compute_total_amount', string='Total Amount', store=True)
    invoice_ids = fields.Many2many("account.move", string="Invoices")
    picking_ids = fields.Many2many('stock.picking', string="Deliveries")
    lead_reference = fields.Char(string="Lead Reference")
    delivery_ids = fields.One2many('stock.picking', 'prescription_id', 'Delivery')
    delivery_count = fields.Integer(compute='_compute_delivery_count', string='Delivery Count', store=True)
    delivered_qty = fields.Integer(string='Delivered Qty')

    @api.depends('prescription_line_ids.total_price')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.prescription_line_ids.mapped('total_price'))

    @api.depends('delivery_ids.prescription_id')
    def _compute_delivery_count(self):
        for rec in self:
            rec.delivery_count = self.env['stock.picking'].search_count([('prescription_id', '=', rec.id)])

    def action_confirm(self):
        self.state = 'confirm'

    def action_cancel(self):
        self.state = 'cancel'

    def action_create_invoice(self):
        vals = self.prepare_invoice_values()

        invoice_id = self.env['account.move'].create(vals)

        line_vals_list = self.prepare_invoice_line_vals(invoice_id)

        line_ids = self.env['account.move.line'].create(line_vals_list)

        # self.invoice_ids = [(0, 0, [invoice_id.id])]

    def prepare_invoice_values(self):
        values = {
            'move_type': 'out_invoice',
            'partner_id': self.patient_id.partner_id.id,
            'partner_shipping_id': self.patient_id.partner_id.id,
            'company_id': self.env.user.company_id.id,
            'invoice_line_ids': [],
            'user_id': self.env.user.id,
            'invoice_date' : self.date
        }
        return values

    def prepare_invoice_line_vals(self, invoice_id):
        line_vals_list = []

        for line in self.prescription_line_ids:
            line_vals = {
                'product_id': line.product_id.id,
                'quantity': line.qty,
                'price_unit': line.price_unit,
                'discount': 0.0,
                'move_id': invoice_id.id,
            }
            line_vals_list.append(line_vals)
            # line_vals_list.append((0, 0, line_vals))
        return line_vals_list

    def action_open_delivery_form(self):
        form_view_id = self.env.ref('stock.view_picking_form').id
        list_view_id = self.env.ref('stock.vpicktree').id

        res = {
            'name': 'Delivery',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'view_id': form_view_id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

        if self.delivery_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = ([('prescription_id', '=', self.id)])
            res['view_id'] = False

        return res

    def action_create_delivery(self):
        picking_vals = self.prepare_picking_values()

        picking_id = self.env['stock.picking'].create(picking_vals)

        line_vals_list = self.prepare_picking_line_vals(picking_id)

        line_ids = self.env['stock.move'].create(line_vals_list)
        print(line_ids)

    def prepare_picking_values(self):
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
        values = {
            'partner_id': self.patient_id.partner_id.id,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': picking_type.default_location_dest_id.id,
            'picking_type_id': picking_type.id,
            'lead_reference' : self.lead_reference,
            'prescription_id': self.id,
        }
        return values

    def prepare_picking_line_vals(self, picking_id):
        line_vals_list = []

        for line in self.prescription_line_ids:
            self.delivered_qty = sum(line.delivery_line_ids.mapped('product_uom_qty'))
            remaining_qty = line.qty - self.delivered_qty
            line_vals = {
                'name' : line.product_id.name,
                'location_id': picking_id.location_id.id,
                'location_dest_id': picking_id.location_dest_id.id,
                'product_id' : line.product_id.id,
                'product_uom_qty' : remaining_qty,
                'picking_id' : picking_id.id,
                'prescription_line_id' : line.id,
            }
            line_vals_list.append(line_vals)
            # line_vals_list.append((0, 0, line_vals))
        return line_vals_list