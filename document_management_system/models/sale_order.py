from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    doc_tag_ids = fields.Many2many('doc.tag.master', string='Tags')
    document_ids = fields.Many2many('documents.custom', string='Documents')
    doc_count = fields.Integer(compute='_compute_get_doc_count', string='Doc Count', store=True)
    doc_line_ids = fields.One2many('document.line', 'sale_order_doc_id', string='Document Lines')
    sys_param_value = fields.Boolean(compute='compute_system_param', string='Sys Param Value for update button')

    @api.onchange('partner_id')
    def onchange_partner_tag(self):
        if self.partner_id:
            self.doc_tag_ids = self.partner_id.tag_ids.ids

    # def button_get_docs(self):
    #     # document_ids = self.order_line.mapped('product_template_id.document_ids')
    #     # tag_dict = {}
    #     # for doc in document_ids:
    #     #     tag_dict.update({doc: doc.tag_ids})
    #     # matched_doc = []
    #     # for doc, tags in tag_dict.items():
    #     #     for so_tag in self.doc_tag_ids:
    #     #         if so_tag.id in tags.ids:
    #     #             matched_doc.append(doc.id)
    #     # self.document_ids = [(6,0, matched_doc)]
    #
    #     matching_docs = self.env['documents.custom']
    #     for line in self.order_line:
    #         record_list = []
    #         product_list = []
    #         docs = line.product_template_id.document_ids.filtered(lambda doc: any(tag in self.doc_tag_ids for tag in doc.tag_ids))
    #         for doc in docs:
    #             record = self.env['document.line'].search([('doc_id', '=', doc.id), ('sale_order_doc_id', '=', self.id)])
    #             if record:
    #                 self.env['document.line'].write({'product_ids' : [(4,line.product_template_id.id)], 'sale_order_doc_id' : self.id})
    #             else:
    #                 self.env['document.line'].create({
    #                     'doc_id' : doc.id,
    #                     'product_ids' : [(6,0,[line.product_template_id.id])],
    #                     'sale_order_doc_id' : self.id
    #                 })
                # else:
                #     dict['product_ids'] = [(6,0,line.product_template_id.id)]
            # matching_docs |= docs
        # list = []
        # for doc in matching_docs:
        #     list.append((0,0,{
        #         'doc_id' : doc.id
        #     }))
        # self.doc_line_ids = list

        # self.document_ids = [(6, 0, matching_docs.ids)]

        # template_id = self.env.ref('document_management_system.email_template_send_sale_person')
        # if self.user_id and self.user_id.login:
        #     template_id.send_mail(self.id, force_send=False)

    def button_get_docs(self):
        matching_docs = self.env['documents.custom']
        for line in self.order_line:
            product = line.product_template_id
            docs = product.document_ids.filtered(lambda doc: any(tag in self.doc_tag_ids for tag in doc.tag_ids))
            matching_docs |= docs

            for rec in docs:
                doc_record = self.env['document.line'].search(
                    [('doc_id', '=', rec.id), ('sale_order_doc_id', '=', self.id)])
                if not doc_record:
                    self.env['document.line'].create(
                        {'doc_id': rec.id, 'sale_order_doc_id': self.id, 'product_ids': [(4, product.id)]})
                else:
                    doc_record.write({'product_ids': [(4, product.id)]})

        self.document_ids = [(6, 0, matching_docs.ids)]

        # template_id = self.env.ref('document_management_system.email_template_send_sale_person')
        # if self.user_id and self.user_id.login:
        #     template_id.send_mail(self.id, force_send=False)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.picking_ids.document_ids = self.document_ids.ids
        # self.set_param()
        return res

    def button_update_docs(self):
        self.message_post(body=f"click update button - {self.env.user.name}")
        matching_docs = self.env['documents.custom']
        for line in self.picking_ids[0].move_ids:
            product = line.product_id
            docs = product.document_ids.filtered(lambda doc: any(tag in self.doc_tag_ids for tag in doc.tag_ids))
            matching_docs |= docs
            self.document_ids = [(6, 0, matching_docs.ids)]

        self.picking_ids[0].document_ids = matching_docs

    @api.depends('document_ids')
    def _compute_get_doc_count(self):
        for rec in self:
            if rec.document_ids:
                rec.doc_count = len(rec.document_ids)

    def compute_system_param(self):
        for rec in self:
            param_value = self.env['ir.config_parameter'].get_param('document_management_system.so_update_button_show_hide1')
            if param_value == '1' :
                rec.sys_param_value = True
            else:
                rec.sys_param_value = False

    # def action_open_add_doc_wizard(self):
    #     view_id = self.env.ref('document_management_system.add_doc_wizard_wizard1').id
    #     # action = self.env["ir.actions.actions"]._for_xml_id("sale.action_view_sale_advance_payment_inv")
    #     return {
    #         'name': 'Add Doc',
    #         'view_mode': 'form',
    #         'res_model': 'add.doc.wizard',
    #         'view_id': view_id,
    #         'type': 'ir.actions.act_window',
    #         'target': 'new',
    #     }

















# (0, 0,  { values })    link to a new record that needs to be created with the given values dictionary
# (1, ID, { values })    update the linked record with id = ID (write values on it)
# (2, ID)                remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)
# (3, ID)                cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)
# (4, ID)                link to existing record with id = ID (adds a relationship)
# (5,)                    unlink all (like using (3,ID) for all linked records). Needs to be a tuple, thus the comma.
# (6, 0, [IDs])          replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)