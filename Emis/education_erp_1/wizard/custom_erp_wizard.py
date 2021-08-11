from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CustomStudentMigrate(models.TransientModel):
    _inherit = "student.migrate"

    department_from_id = fields.Many2one('op.department', 'From Department', required=True)
    department_to_id = fields.Many2one('op.department', 'To Department', required=True)


class CustomGenerateTimeTable(models.TransientModel):
    _inherit = 'generate.time.table'

    faculty = fields.Many2one('edu.faculty', 'Faculty Name', required=True)
    department_id = fields.Many2one(
        'op.department', 'Department',
        default=lambda self:
        self.env.user.dept_id and self.env.user.dept_id.id or False)

    # additional_exam_result = fields.One2many("additional.exam.result",
    #                                          string="additional exam result", compute='_compute_exam',
    #                                          help='Total Additional exam')
    #
    # @api.depends('standard_id', 'student_id')
    # def _compute_exam(self):
    #     student_obj = self.env['additional.exam.result']
    #     for rec in self:
    #         rec.additional_exam_result = student_obj. \
    #             search([('standard_id', '=', rec.standard_id.id),
    #                     ('student_id', '=', rec.student_id.id),
    #                     ('active', '=', True)])

    @api.onchange('batch_id')
    def onchange_batch_id(self):
        session_obj = self.env['op.session']
        time_list = []
        for rec in self:
            if rec.batch_id:
                session_ids = session_obj.search([('batch_id', '=',
                                                   rec.batch_id.id)])
                for line in session_ids:
                    print(line)
                    if line.type == 'Monday':
                        num = '0'
                    elif line.type == 'Tuesday':
                        num = '1'
                    elif line.type == 'Wednesday':
                        num = '2'
                    elif line.type == 'Thursday':
                        num = '3'
                    elif line.type == 'Friday':
                        num = '4'
                    elif line.type == 'Saturday':
                        num = '5'
                    else:
                        num = '6'
                    line_vals = (0, 0, {
                                        'faculty_id': line.faculty_id.id,
                                        'subject_id': line.subject_id.id,
                                        'timing_id': line.timing_id.id,
                                        'classroom_id': line.classroom_id.id,
                                        'day': num
                                        })
                    time_list.append(line_vals)

                    new_list = []
                    for i in time_list:
                        if i not in new_list:
                            new_list.append(i)

                    time_list = new_list
                print(time_list)
            rec.time_table_lines = [(5,)]
            rec.time_table_lines = time_list
        return {
            'type': 'ir.actions.act_window',
            'res_model': "generate.time.table",
            'res_id': rec.id,
            'view_mode': 'form',
            'name': 'Generate Sessions',
            'target': 'inline'
        }


class CustomGenTimeTableLine(models.TransientModel):
    _inherit = 'gen.time.table.line'

    department_id = fields.Many2one(
        'op.department', 'Department', related='gen_time_table.department_id', store=True)
    course_id = fields.Many2one('op.course', 'Course', related='gen_time_table.course_id', store=True)
    batch_id = fields.Many2one('op.batch', 'Batch', related='gen_time_table.batch_id', store=True)

    faculty_id = fields.Many2one('op.faculty', 'Faculty', required=True)
