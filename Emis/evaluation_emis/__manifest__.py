# See LICENSE file for full copyright and licensing details.

{
    "name": "Evaluation Emis",
    "version": "14.0.1",
    "author": "nova",
    "website": "",
    "category": "evaluation",
    "license": "AGPL-3",
    "complexity": "easy",
    "images": ["static/description/Evaluation1.jpg"],
    "depends": ["openeducat_core", "rating", "openeducat_exam"],
    "data": [
        "security/evaluation_security.xml",
        "security/ir.model.access.csv",
        "views/school_evaluation_view.xml",
        "views/templates.xml",
        "reports/student_evaluation.xml",
        "reports/student_report.xml",
        "menus/emis_eval_menu.xml"
    ],
    "installable": True,
    "application": True,
}
