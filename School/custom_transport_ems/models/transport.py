# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


# ------------------------------------
# Custom Transport Registration
# ------------------------------------
class CustomTransportRegistration(models.Model):
    _inherit = 'transport.registration'

    @api.depends("transport_fees", "paid_amount")
    def _compute_remain_amount(self):
        # due amount
        self.remain_amt = self.transport_fees - self.paid_amount


    reg_date = fields.Date(
        "Registration Date",
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="Start Date of registration",
        default=fields.Date.context_today
    )

    reg_end_date = fields.Date(
        "Registration End Date",
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="Start Date of registration",
    )
    registration_month = fields.Integer("Registration For Months")
    monthly_amount = fields.Float(
        "Monthly Amount", readonly=False, help="Enter monthly amount"
    )
    paid_amount = fields.Float("Paid Amount", readonly=False, help="Amount Paid")
    remain_amt = fields.Float(
        string="Due Amount",
        compute="_compute_remain_amount",
        readonly=False,
        help="Amount Remaining")
    transport_fees = fields.Float(
        compute="_compute_transport_fees",
        string="Transport Fees",
        help="Transport fees",
    )

    @api.onchange("registration_month", "reg_date", "reg_end_date")
    def onchange_registration_month(self):
        self.reg_end_date = self.reg_date + relativedelta(
            months=self.registration_month)

    def trans_regi_confirm(self):
        trans_obj = self.env["student.transport"]
        prt_obj = self.env["student.student"]
        stu_prt_obj = self.env["transport.participant"]
        vehi_obj = self.env["fleet.vehicle"]
        for rec in self:
            if rec.registration_month <= 0:
                raise UserError(
                    _(
                        """Error!
                    Registration months must be 1 or more then one month!"""
                    )
                )
            person = int(rec.vehicle_id.vehi_participants_ids) + 1
            # if rec.vehicle_id.capacity < person:
            #     raise UserError(_("There is No More vacancy on this vehicle!"))

            rec.write({"state": "confirm", "remain_amt": rec.transport_fees})
            # calculate amount and Registration End date
            tr_start_date = rec.reg_date
            ed_date = rec.name.end_date
            tr_end_date = tr_start_date + relativedelta(
                months=rec.registration_month)
            if tr_end_date > ed_date:
                raise UserError(
                    _(
                        """
For this much Months Registration is not Possible because Root
end date is Early!"""
                    )
                )
            # make entry in Transport
            dict_prt = {
                "stu_pid_id": str(rec.student_id.pid),
                "amount": rec.monthly_amount,
                "transport_id": rec.name.id,
                "tr_end_date": tr_end_date,
                "name": rec.student_id.id,
                "months": rec.registration_month,
                "tr_reg_date": rec.reg_date,
                "state": "running",
                "vehicle_id": rec.vehicle_id.id,
            }
            temp = stu_prt_obj.sudo().create(dict_prt)
            # make entry in Transport vehicle.
            vehi_participants_list = []
            for prt in rec.vehicle_id.vehi_participants_ids:
                vehi_participants_list.append(prt.id)
            flag = True
            for prt in vehi_participants_list:
                data = stu_prt_obj.browse(prt)
                if data.name.id == rec.student_id.id:
                    flag = False
            if flag:
                vehi_participants_list.append(temp.id)
            vehicle_rec = vehi_obj.browse(rec.vehicle_id.id)
            vehicle_rec.sudo().write(
                {"vehi_participants_ids": [(6, 0, vehi_participants_list)]}
            )
            # make entry in student.
            transport_list = []
            for root in rec.student_id.transport_ids:
                transport_list.append(root.id)
            transport_list.append(temp.id)
            student_rec = prt_obj.browse(rec.student_id.id)
            student_rec.sudo().write(
                {"transport_ids": [(6, 0, transport_list)]}
            )
            # make entry in transport.
            trans_participants_list = []
            for prt in rec.name.trans_participants_ids:
                trans_participants_list.append(prt.id)
            trans_participants_list.append(temp.id)
            stu_tran_rec = trans_obj.browse(rec.name.id)
            stu_tran_rec.sudo().write(
                {"trans_participants_ids": [(6, 0, trans_participants_list)]}
            )


# ------------------------------------
# Custom Res Partner
# ------------------------------------
class ResPartner(models.Model):
    _inherit = "res.partner"

    licence_no = fields.Char("License No", help="Enter License No.")

    _sql_constraints = [
        ('licence_unique', 'unique(licence_no)',
         'licence should be unique!')
    ]
