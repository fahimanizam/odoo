# See LICENSE file for full copyright and licensing details.

{
    "name": "School Quiz",
    "version": "14.0.1",
    "author": "Nova",
    "website": "",
    "images": ["static/description/SchoolQuiz.png"],
    # "category": "School Management",
    # "license": "AGPL-3",
    # "complexity": "easy",
    # "summary": "A Module For Quiz In School",
    # 'images': ['static/description/quiz.png'],
    "depends": ["base","school", "survey"],
    "data": [
        # "security/quiz_security.xml",
        "report/report_view.xml",
        "report/quiz_result_report.xml",
        "report/student_quiz_result_report.xml",
        "security/ir.model.access.csv",
        "views/quiz_view.xml",
        "views/quiz_question_template.xml",
    ],
    "installable": True,
    "application": True,
}
