# -*- coding: utf-8 -*-
from odoo import api, fields, models


# ------------------------------------
# Op Student inherited Class
# ------------------------------------
class OpStudent(models.Model):
    _inherit = 'op.student'

    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")

    def create_student_user(self):
        user_group = self.env.ref("base.group_user") or False
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'login': record.email,
                    'groups_id': user_group,
                    'is_student': True,
                    'tz': self._context.get('tz'),
                })
                record.user_id = user_id