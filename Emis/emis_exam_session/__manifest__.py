# -*- coding: utf-8 -*-

{
    "name": "Exam Session & Answer Submission",
    # ------------------------------
    "version": "14.0.1",
    # ------------------------------
    "author": "Nova",
    # ------------------------------
    "depends": ["base", "website", "openeducat_core"],
    # ------------------------------
    "data": [
        "security/ir.model.access.csv",
        # ------------------------------
        "menu/exam_session_menu.xml",
        # ------------------------------
        "views/exam_session_view.xml",
        "views/student_input_view.xml",
        # ------------------------------
        "website/website_menus.xml",
        "website/web_asset.xml",
        "website/answer_submission.xml",
        # ------------------------------
    ],
}
