# See LICENSE file for full copyright and licensing details.

from lxml import etree

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class EvaluationEmis(models.Model):
    """Defining School Evaluation."""

    _name = "evaluation.emis"
    _description = "School Evaluation details"
    _rec_name = "type"

    @api.depends("eval_line_ids")
    def _compute_total_points(self):
        """Method to compute evaluation points"""
        for rec in self:
            if rec.eval_line_ids:
                rec.total = sum(
                    line.point_id.rating
                    for line in rec.eval_line_ids
                    if line.point_id.rating
                )

    student_id = fields.Many2one(
        "op.student", "Student Name", help="Select Student"
    )

    teacher_id = fields.Many2one(
        "op.faculty", "Faculty", help="Select teacher"
    )

    standard_id = fields.Many2one(
        "op.batch", "Batch", help="Select standard for exam"
    )

    type = fields.Selection(
        [("student", "Student"), ("faculty", "Faculty")],
        "User Type",
        required=True,
        help="Type of evaluation",
    )

    remarks = fields.Text(string="Remarks")
    total_attendance = fields.Integer(string="Total attendance (Days)", default=0)
    present = fields.Integer(string="Present (Days)", default=0)
    date = fields.Date(
        "Evaluation Date",
        required=True,
        help="Evaluation Date",
        default=fields.Date.context_today,
    )
    eval_line_ids = fields.One2many(
        "evaluation.emis.line",
        "eval_id",
        "Questionnaire",
        help="Enter evaluation details",
    )

    total = fields.Float(
        "Total Points",
        compute="_compute_total_points",
        method=True,
        help="Total Points Obtained",
        store="True",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("start", "In Progress"),
            ("finished", "Finish"),
            ("cancelled", "Cancel"),
        ],
        "State",
        readonly=True,
        default="draft",
        help="State of evaluation line",
    )
    username = fields.Many2one(
        "res.users",
        "User",
        readonly=True,
        default=lambda self: self.env.user,
        help="Related user",
    )
    active = fields.Boolean(
        "Active", default=True, help="Activate/Deactivate record"
    )

    @api.model
    def default_get(self, fields):
        """Override method to get default value of teacher"""
        res = super(EvaluationEmis, self).default_get(fields)
        if res.get("type") == "student":
            hr_emp_rec = self.env["op.faculty"].search(
                [("user_id", "=", self._uid)]
            )
            res.update({"teacher_id": hr_emp_rec.id})
        return res

    @api.model
    def fields_view_get(
            self, view_id=None, viewtype="form", toolbar=False, submenu=False
    ):
        """Inherited this method to hide the create,edit button from list"""

        res = super(EvaluationEmis, self).fields_view_get(
            view_id=view_id,
            view_type=viewtype,
            toolbar=toolbar,
            submenu=submenu,
        )
        teacher_group = self.env.user.has_group("openeducat_core.group_op_faculty")
        doc = etree.XML(res["arch"])
        if teacher_group:
            if viewtype == "tree":
                nodes = doc.xpath("//tree[@name='teacher_evaluation']")
                for node in nodes:
                    node.set("create", "true")
                    node.set("edit", "true")
                res["arch"] = etree.tostring(doc)
            if viewtype == "form":
                nodes = doc.xpath("//form[@name='teacher_evaluation']")
                for node in nodes:
                    node.set("create", "true")
                    node.set("edit", "true")
                res["arch"] = etree.tostring(doc)
        return res

    def get_record(self):
        """Method to get the evaluation questions"""
        eval_temp_obj = self.env["evaluation.emis.template"]
        for rec in self:
            eval_list = []
            eval_temps_rec = eval_temp_obj.search([("type", "=", rec.type)])
            for eval_temp in eval_temps_rec:
                eval_list.append((0, 0, {"stu_eval_id": eval_temp.id}))
            if rec.eval_line_ids:
                rec.write({"eval_line_ids": [(5, 0, 0)]})
            rec.write({"eval_line_ids": eval_list})
        return True

    def set_start(self):
        """change state to start"""
        for rec in self:
            if not rec.eval_line_ids:
                raise ValidationError(
                    _(
                        'Please Get the Questions First!\
            \nTo Get the Questions please click on "Get Questions" Button!'
                    )
                )
        self.state = "start"

    def set_finish(self):
        """Change state to finished"""
        for rec in self:
            if [
                line.id
                for line in rec.eval_line_ids
                if (not line.point_id or not line.rating)
            ]:
                raise ValidationError(
                    _(
                        """
                You can't mark the evaluation as Finished untill
                the Rating/Remarks are not added for all the Questions!"""
                    )
                )
        self.state = "finished"

    def set_cancel(self):
        """Change state to cancelled"""
        self.state = "cancelled"

    def set_draft(self):
        """Changes state to draft"""
        self.state = "draft"

    def unlink(self):
        """Inherited unlink method to check state at record deletion"""
        for rec in self:
            if rec.state in ["start", "finished"]:
                raise ValidationError(
                    _(
                        """
                    You can delete record in unconfirmed state only!"""
                    )
                )
        return super(EvaluationEmis, self).unlink()


class StudentEvaluationLine(models.Model):
    """Defining School Evaluation Line."""

    _name = "evaluation.emis.line"
    _description = "School Evaluation Line Details"
    _order = "stu_eval_id asc"

    eval_id = fields.Many2one(
        "evaluation.emis", "Evaluation id", help="Select school evaluation"
    )

    category_id = fields.Many2one('evaluation.emis.template.category', 'Category')

    stu_eval_id = fields.Many2one(
        "evaluation.emis.template",
        "Question",
        help="Select evaluation question",
    )
    point_id = fields.Many2one(
        "rating.rating",
        "Grade Point",
        domain="[('template_id', '=', stu_eval_id)]",
        help="Evaluation point",
    )
    rating = fields.Char("Letter Grade", help="Enter remark")

    _sql_constraints = [
        (
            "number_uniq",
            "unique(eval_id, stu_eval_id)",
            "Questions already exist!",
        )
    ]

    @api.onchange("point_id")
    def onchange_point(self):
        """Method to get rating point based on rating"""
        self.rating = False
        if self.point_id:
            self.rating = self.point_id.feedback


class SchoolEvaluationTemplate(models.Model):
    """Defining School Evaluation Template."""

    _name = "evaluation.emis.template"
    _description = "School Evaluation Template Details"
    _order = "desc asc"
    _rec_name = "desc"

    desc = fields.Char("Description", required=True, help="Description")
    type = fields.Selection(
        [("faculty", "Faculty"), ("student", "Student")],
        "User Type",
        required=True,
        default="faculty",
        help="Type of Evaluation",
    )

    category_id = fields.Many2one('evaluation.emis.template.category', 'Category')

    rating_line = fields.One2many(
        "rating.rating", "template_id", "Rating", help="Rating"
    )


class SchoolEvaluationTemplateCategory(models.Model):
    """Defining School Evaluation Template."""
    _name = "evaluation.emis.template.category"
    _description = "School Evaluation Template Category Details"
    _rec_name = 'category_name'

    category_name = fields.Char(string='Category Name', required=True)
    _sql_constraints = [
        ('category_name_uniq', 'unique(category_name)',
         'Category already exist!'),
    ]


class RatingRating(models.Model):
    """Defining Rating."""

    _inherit = "rating.rating"
    _description = "Rating"

    @api.model
    def create(self, vals):
        """Set Document model name for rating."""
        res_model_rec = self.env["ir.model"].search(
            [("model", "=", "evaluation.emis.template")]
        )
        vals.update({"res_model_id": res_model_rec.id})
        res = super(RatingRating, self).create(vals)
        return res

    @api.depends("res_model", "res_id")
    def _compute_res_name(self):
        """Override this method to set the alternate rec_name as rating"""

        for rate in self:
            if rate.res_model == "evaluation.emis.template":
                rate.res_name = rate.rating
            else:
                super(RatingRating, self)._compute_res_name()

    template_id = fields.Many2one(
        "evaluation.emis.template", "Stud", help="Ratings"
    )


class StudentExtend(models.Model):
    _inherit = "op.student"

    def set_alumni(self):
        student_eval_obj = self.env["emis.evaluation"]
        for rec in self:
            student_eval_rec = student_eval_obj.search(
                [("type", "=", "student"), ("student_id", "=", rec.id)]
            )
            if student_eval_rec:
                student_eval_rec.active = False
        return super(StudentExtend, self).set_alumni()
