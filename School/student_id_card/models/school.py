# -*- coding: utf-8 -*-
import qrcode

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SchoolSchool(models.Model):
    ''' Inheriting School Information'''

    _inherit = 'school.school'

    def get_full_address(self, *kw):
        address_list = []
        for k in kw:
            if k is not self:
                if k:
                    address_list.append(str(k))
        full_address = ', '.join(address_list)
        return full_address








