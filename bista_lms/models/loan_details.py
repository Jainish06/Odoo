from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

class LoanDetails(models.Model):
    _name = 'loan.details'
    _description = 'Loan Details and EMI'

    name = fields.Char(string='Loan Num')
    partner_id = fields.Many2one('res.partner', string='Customer')
    loan_period = fields.Integer(string='Tenure')
    interest_rate_ids = fields.One2many('loan.interest.rate', 'loan_id', string='Interest Rates')
    loan_start_date = fields.Date(string='Start Date')
    loan_end_date = fields.Date(string='End Date')
    emi_pay_date = fields.Integer(string='EMI Payment Date')
    emi_amount = fields.Float(compute='_compute_emi', string='EMI Amount', store=True)
    emi_line_ids = fields.One2many('loan.emi.lines', 'loan_id', string='EMI Lines')
    total_interest_amt = fields.Float(compute='_compute_compound_interest', string='Total Interest Amount', store=True)
    paid_interest_amt = fields.Float(string='Interest Paid')
    pending_interest_amt = fields.Float(string='Pending Interest Amount')
    total_principle_amt = fields.Float(string='Total Principle Amount')
    paid_principle_amt = fields.Float(string='Principle Paid')
    pending_principle_amt = fields.Float(string='Pending Principle Amount')
    curr_interest_rate = fields.Float(string='Current Interest Rate')
    move_ids = fields.One2many('account.move', 'loan_id', 'Invoice')
    invoice_count = fields.Integer(compute='_compute_invoice_count', string='Invoice count', store=True)


    @api.onchange('loan_period', 'loan_start_date')
    def onchange_end_date(self):
        if self.loan_period and self.loan_start_date:
            self.loan_end_date = self.loan_start_date + relativedelta(months=self.loan_period)

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val.update({'name': self.env['ir.sequence'].next_by_code('loan.details')})
        res = super(LoanDetails, self).create(vals_list)
        return res

    @api.depends('total_principle_amt', 'emi_amount', 'loan_period')
    def _compute_compound_interest(self):
        for rec in self:
            if rec.total_principle_amt and rec.emi_amount and rec.loan_period:
                rec.total_interest_amt = rec.emi_amount * rec.loan_period - rec.total_principle_amt

    @api.depends('total_principle_amt', 'loan_period', 'curr_interest_rate')
    def _compute_emi(self):
        for rec in self:
            if rec.total_principle_amt and rec.loan_period and rec.curr_interest_rate:
                r = rec.curr_interest_rate/1200
                rec.emi_amount = (rec.total_principle_amt * r * ((1 + r) ** rec.loan_period))/(((1 + r) ** rec.loan_period) - 1)

    @api.depends('move_ids.loan_id')
    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = len(self.move_ids)

    def action_generate_emi_lines(self):
        emi_amt = self.emi_amount
        principle_amt = self.total_principle_amt
        emi_date = self.loan_start_date
        monthly_int_rate = self.curr_interest_rate/1200
        emi_lines = []
        if monthly_int_rate:
            for month in range(self.loan_period):
                curr_interest = principle_amt * monthly_int_rate
                curr_principle_amt = emi_amt - curr_interest
                curr_pay_date = emi_date
                principle_amt -= curr_principle_amt
                emi_line_id = self.env['loan.emi.lines'].create({
                    'loan_id' : self.id,
                    'date_paid' : curr_pay_date,
                    'paid_interest_amt' : curr_interest,
                    'paid_principle_amt' : curr_principle_amt,
                    'total_amt' : emi_amt,
                }).id
                emi_lines.append(emi_line_id)
                emi_date += relativedelta(months=1)
            self.emi_line_ids = [(6,0,emi_lines)]

    def _emi_auto_payment(self):
        today = date.today()
        records = self.search([])
        if records:
            for rec in records:
                emi_line = rec.emi_line_ids.filtered(lambda line : line.date_paid == today)
                if emi_line:
                    vals = rec.prepare_invoice_values()
                    invoice_id = self.env['account.move'].create(vals)
                    line_vals_list = rec.prepare_invoice_line_vals(invoice_id)
                    line_ids = self.env['account.move.line'].create(line_vals_list)
                    if invoice_id and rec.invoice_count>=1:
                        rec.move_ids.action_post()
                        emi_line.state = 'invoice_generated'
                        if rec.partner_id.email:
                            template_id = self.env.ref('bista_lms.emi_invoiced_email_template')
                            template_id.send_mail(emi_line.id, force_send=True)

    def _emi_reminder(self):
        today = date.today()
        check_date = today + relativedelta(days=2)
        records = self.search([])
        if records:
            for rec in records:
                emi_line = rec.emi_line_ids.filtered(lambda line: line.date_paid == check_date)
                if emi_line:
                    if rec.partner_id.email:
                        template_id = self.env.ref('bista_lms.emi_reminder_email_template')
                        template_id.send_mail(emi_line.id, force_send=True)

    def prepare_invoice_values(self):
        values = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'partner_shipping_id': self.partner_id.id,
            'company_id': self.env.user.company_id.id,
            'user_id': self.env.user.id,
            'invoice_date': date.today(),
            'loan_id' : self.id
        }
        return values

    def prepare_invoice_line_vals(self, invoice_id):
        line_vals_list = []
        today = date.today()
        product = self.env['product.product'].search([('name', '=', 'EMI')])
        emi_lines = self.emi_line_ids.filtered(lambda line: line.date_paid == today)
        for line in emi_lines:
            line_vals = {
                'product_id': product.id,
                'quantity': 1,
                'price_unit': line.total_amt,
                'move_id': invoice_id.id,
            }
            line_vals_list.append(line_vals)
            # line_vals_list.append((0, 0, line_vals))
        return line_vals_list

    def action_open_invoice_form(self):
        form_view_id = self.env.ref('account.view_move_form').id
        list_view_id = self.env.ref('account.view_out_invoice_tree').id

        res = {
            'name': 'Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': form_view_id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

        if self.invoice_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = ([('loan_id', '=', self.id)])
            res['view_id'] = False

        return res