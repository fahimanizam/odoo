# -*- coding: utf-8 -*-

{
    "name": "News Carousel",
    # ------------------------------
    "version": "14.0.1",
    # ------------------------------
    "author": "Nova",
    # ------------------------------
    "depends": ["base", "website","website_blog"],
    # ------------------------------
    "data": [
        "security/ir.model.access.csv",
        # ------------------------------
        "menu/news_carousel_menu.xml",
        # ------------------------------
        "views/news_carousel_view.xml",
        # ------------------------------
        # "website/website_menus.xml",
        "website/web_asset.xml",
        "website/web_news_carousel.xml",
        # ------------------------------
    ],
}
