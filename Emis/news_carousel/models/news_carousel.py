# -*- coding: utf-8 -*-
from odoo import api, fields, models


# ------------------------------------
# News Carousel Class
# ------------------------------------
class NewsCarousel(models.Model):
    _name = 'news.carousel'
    _description = 'News Carousel'

    news_headings = fields.Char('News headings', required=True)
    description = fields.Html('Description')

