#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from datetime import datetime
from odoo.exceptions import ValidationError

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class SaleCardReportDaily(models.AbstractModel):
    _name = 'report.daily_sale_report.daily_template_id'

    @api.model
    def _get_report_values(self, docids, data=None):
        dailylines=data.get('dailylines',[])
        docargs = {
            'dailylines': dailylines,
        }
        return docargs




