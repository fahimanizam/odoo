# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api, _
from odoo.exceptions import Warning as UserError
from datetime import date
from odoo.exceptions import ValidationError


# ------------------------------------
# Custom Daily Attendance Class
# ------------------------------------
class CustomDailyAttendance(models.Model):
    _inherit = 'daily.attendance'

    @api.depends('total_presence')
    def _compute_present_percentage(self):
        for rec in self:
            present_p = 0
            if rec.total_student > 0 and rec.total_presence > 0:
                present_p = int((rec.total_presence / rec.total_student) * 100)
            rec.total_percentage = str(present_p) + "%"

    total_percentage = fields.Char(compute="_compute_present_percentage",
                                   store=True,
                                   string='Percentage of Present Student',
                                   help="Present Student Percentage")


# ------------------------------------
# Custom Daily Attendance Class
# ------------------------------------
class DailySubjectAttendance(models.Model):
    '''Defining Daily Subject Attendance Information.'''

    _description = 'Daily Subject Attendance'
    _name = 'daily.subject.attendance'
    _rec_name = 'standard_id'

    # _inherit = ['attendance.sheet','attendance.sheet.line','daily.attendance.line']

    @api.depends('student_ids')
    def _compute_total(self):
        '''Method to compute total student'''
        for rec in self:
            rec.total_student = len(rec.student_ids and
                                    rec.student_ids.ids or [])

    @api.depends('student_ids')
    def _compute_present(self):
        '''Method to count present students.'''
        for rec in self:
            count = 0
            for att in rec.student_ids:
                if att.is_present:
                    count += 1
            rec.total_presence = count

    @api.depends('student_ids')
    def _compute_absent(self):
        '''Method to count absent students'''
        for rec in self:
            count_fail = 0
            if rec.student_ids:
                for att in rec.student_ids:
                    if att.is_absent:
                        count_fail += 1
                rec.total_absent = count_fail

    @api.constrains('date')
    def validate_date(self):
        if self.date > date.today():
            raise ValidationError(_("Date should be less than or equal to\
            current date!"))

    @api.depends('total_presence')
    def _compute_present_percentage(self):
        for rec in self:
            present_p = 0
            if rec.total_student > 0 and rec.total_presence > 0:
                present_p = int((rec.total_presence / rec.total_student) * 100)
            rec.total_percentage = str(present_p) + "%"

    total_percentage = fields.Char(compute="_compute_present_percentage",
                                   store=True,
                                   string='Percentage of Present Student',
                                   help="Present Student Percentage")

    date = fields.Date("Date", help="Current Date",
                       default=lambda *a: time.strftime('%Y-%m-%d'))
    standard_id = fields.Many2one('school.standard', 'Academic Class',
                                  required=True, help="Select Standard",
                                  states={'validate': [('readonly', True)]})

    subject_id = fields.Many2one(
        "subject.subject", "Subject", required=True, help="Select Subject"
    )
    student_ids = fields.One2many('daily.subject.attendance.line', 'standard_id',
                                  'Students',
                                  states={'validate': [('readonly', True)],
                                          'draft': [('readonly', False)]})
    user_id = fields.Many2one('school.teacher', 'Faculty',
                              help="Select Teacher", ondelete='restrict',
                              states={'validate': [('readonly', True)]})
    state = fields.Selection([('draft', 'Draft'), ('validate', 'Validate')],
                             'State', readonly=True, default='draft')
    total_student = fields.Integer(compute="_compute_total",
                                   store=True,
                                   help="Total Students in class",
                                   string='Total Students')
    total_presence = fields.Integer(compute="_compute_present",
                                    store=True, string='Present Students',
                                    help="Present Student")
    total_absent = fields.Integer(compute="_compute_absent",
                                  store=True,
                                  string='Absent Students',
                                  help="Absent Students")

    _sql_constraints = [
        ('attend_unique', 'unique(standard_id,subject_id,user_id,date)',
         'Attendance should be unique!')
    ]

    @api.onchange('standard_id')
    def onchange_standard_id(self):
        '''Method to get standard of student selected'''
        stud_obj = self.env['student.student']
        student_list = []
        for rec in self:
            if rec.standard_id:
                stud_ids = stud_obj.search([('standard_id', '=',
                                             rec.standard_id.id),
                                            ('state', '=', 'done')])
                for stud in stud_ids:
                    student_leave = self.env['studentleave.request'
                    ].search([('state', '=',
                               'approve'),
                              ('student_id', '=',
                               stud.id),
                              ('standard_id', '=',
                               rec.standard_id.id),
                              ('start_date', '<=',
                               rec.date),
                              ('end_date', '>=',
                               rec.date)
                              ])
                    stud_vals_abs = (0, 0, {'roll_no': stud.roll_no,
                                            'stud_id': stud.id,
                                            'is_absent': True
                                            })
                    stud_vals = (0, 0, {'roll_no': stud.roll_no,
                                        'stud_id': stud.id,
                                        'is_present': True
                                        })
                    if student_leave:

                        student_list.append(stud_vals_abs)
                    else:
                        student_list.append(stud_vals)
            rec.student_ids = [(5,)]
            rec.student_ids = student_list

    @api.model
    def create(self, vals):
        student_list = []
        stud_obj = self.env['student.student']
        standard_id = vals.get('student_id')
        date = vals.get('date')
        stud_ids = stud_obj.search([('standard_id', '=',
                                     vals.get('standard_id')),
                                    ('state', '=', 'done')])
        for stud in stud_ids:
            line_vals = {'roll_no': stud.roll_no,
                         'stud_id': stud.id,
                         'is_present': True
                         }
            if vals.get('student_ids') and not vals.get(
                    'student_ids')[0][2].get('present_absentcheck'):
                student_leave = self.env['studentleave.request'
                ].search([('state', '=',
                           'approve'),
                          ('student_id', '=',
                           stud.id),
                          ('standard_id', '=',
                           standard_id),
                          ('start_date', '<=',
                           date),
                          ('end_date', '>=',
                           date)
                          ])
                if student_leave:
                    line_vals.update({'is_absent': True})
            student_list.append((0, 0, line_vals))
        vals.update({'student_ids': student_list})
        return super(DailySubjectAttendance, self).create(vals)

    def attendance_draft(self):
        '''Change the state of attendance to draft'''
        att_sheet_obj = self.env['attendance.sheet']
        academic_year_obj = self.env['academic.year']
        academic_month_obj = self.env['academic.month']

        for rec in self:
            if not rec.date:
                raise UserError(_('Please enter todays date.'))
            year_search_ids = academic_year_obj.search([('code', '=',
                                                         rec.date.year)])
            month_search_ids = academic_month_obj.search([('code', '=',
                                                           rec.date.month)])
            sheet_ids = att_sheet_obj.search(
                [('standard_id', '=', rec.standard_id.id),
                 ('month_id', '=', month_search_ids.id),
                 ('year_id', '=', year_search_ids.id)])
            if sheet_ids:
                for data in sheet_ids:
                    for attendance_id in data.attendance_ids:
                        date = rec.date
                        if date.day == 1:
                            dic = {'one': False}
                        elif date.day == 2:
                            dic = {'two': False}
                        elif date.day == 3:
                            dic = {'three': False}
                        elif date.day == 4:
                            dic = {'four': False}
                        elif date.day == 5:
                            dic = {'five': False}
                        elif date.day == 6:
                            dic = {'six': False}
                        elif date.day == 7:
                            dic = {'seven': False}
                        elif date.day == 8:
                            dic = {'eight': False}
                        elif date.day == 9:
                            dic = {'nine': False}
                        elif date.day == 10:
                            dic = {'ten': False}
                        elif date.day == 11:
                            dic = {'one_1': False}
                        elif date.day == 12:
                            dic = {'one_2': False}
                        elif date.day == 13:
                            dic = {'one_3': False}
                        elif date.day == 14:
                            dic = {'one_4': False}
                        elif date.day == 15:
                            dic = {'one_5': False}
                        elif date.day == 16:
                            dic = {'one_6': False}
                        elif date.day == 17:
                            dic = {'one_7': False}
                        elif date.day == 18:
                            dic = {'one_8': False}
                        elif date.day == 19:
                            dic = {'one_9': False}
                        elif date.day == 20:
                            dic = {'one_0': False}
                        elif date.day == 21:
                            dic = {'two_1': False}
                        elif date.day == 22:
                            dic = {'two_2': False}
                        elif date.day == 23:
                            dic = {'two_3': False}
                        elif date.day == 24:
                            dic = {'two_4': False}
                        elif date.day == 25:
                            dic = {'two_5': False}
                        elif date.day == 26:
                            dic = {'two_6': False}
                        elif date.day == 27:
                            dic = {'two_7': False}
                        elif date.day == 28:
                            dic = {'two_8': False}
                        elif date.day == 29:
                            dic = {'two_9': False}
                        elif date.day == 30:
                            dic = {'two_0': False}
                        elif date.day == 31:
                            dic = {'three_1': False}
                        attendance_id.write(dic)
            rec.state = 'draft'
        return True

    def attendance_validate(self):
        '''Method to validate attendance.'''
        sheet_line_obj = self.env['attendance.sheet.line']
        acadmic_year_obj = self.env['academic.year']
        acadmic_month_obj = self.env['academic.month']
        attendance_sheet_obj = self.env['attendance.sheet']

        for line in self:
            year_ids = acadmic_year_obj.search(
                [('date_start', '<=', line.date),
                 ('date_stop', '>=', line.date)])
            month_ids = acadmic_month_obj.search(
                [('date_start', '<=', line.date),
                 ('date_stop', '>=', line.date),
                 ('year_id', 'in', year_ids.ids)])
            if month_ids:
                month_data = month_ids
                att_sheet_ids = attendance_sheet_obj.search([('month_id', 'in',
                                                              month_ids.ids),
                                                             ('year_id', 'in',
                                                              year_ids.ids)])
                attendance_sheet_id = (att_sheet_ids and att_sheet_ids[0] or
                                       False)
                date = line.date
                if not attendance_sheet_id:
                    sheet = {'name': (month_data.name + '-' +
                                      str(line.date.year)),
                             'standard_id': line.standard_id.id,
                             'user_id': line.user_id.id,
                             'month_id': month_data.id,
                             'year_id': year_ids and year_ids.id or False}
                    attendance_sheet_id = attendance_sheet_obj.create(sheet)
                    for student_id in line.student_ids:
                        line_dict = {'roll_no': student_id.roll_no,
                                     'standard_id': attendance_sheet_id.id,
                                     'name': student_id.stud_id.student_name}
                        sheet_line_obj.create(line_dict)
                        for student_id in line.student_ids:
                            search_id = sheet_line_obj. \
                                search([('roll_no', '=', student_id.roll_no)])
                            # compute attendance of each day
                            if date.day == 1 and student_id.is_absent:
                                val = {'one': False}

                            elif date.day == 1 and not student_id.is_absent:
                                val = {'one': True}

                            elif date.day == 2 and student_id.is_absent:
                                val = {'two': False}

                            elif date.day == 2 and not student_id.is_absent:
                                val = {'two': True}

                            elif date.day == 3 and student_id.is_absent:
                                val = {'three': False}

                            elif date.day == 3 and not student_id.is_absent:
                                val = {'three': True}

                            elif date.day == 4 and student_id.is_absent:
                                val = {'four': False}

                            elif date.day == 4 and not student_id.is_absent:
                                val = {'four': True}

                            elif date.day == 5 and student_id.is_absent:
                                val = {'five': False}

                            elif date.day == 5 and not student_id.is_absent:
                                val = {'five': True}

                            elif date.day == 6 and student_id.is_absent:
                                val = {'six': False}

                            elif date.day == 6 and not student_id.is_absent:
                                val = {'six': True}

                            elif date.day == 7 and student_id.is_absent:
                                val = {'seven': False}

                            elif date.day == 7 and not student_id.is_absent:
                                val = {'seven': True}

                            elif date.day == 8 and student_id.is_absent:
                                val = {'eight': False}

                            elif date.day == 8 and not student_id.is_absent:
                                val = {'eight': True}

                            elif date.day == 9 and student_id.is_absent:
                                val = {'nine': False}

                            elif date.day == 9 and not student_id.is_absent:
                                val = {'nine': True}

                            elif date.day == 10 and student_id.is_absent:
                                val = {'ten': False}

                            elif date.day == 10 and not student_id.is_absent:
                                val = {'ten': True}

                            elif date.day == 11 and student_id.is_absent:
                                val = {'one_1': False}

                            elif date.day == 11 and not student_id.is_absent:
                                val = {'one_1': True}

                            elif date.day == 12 and student_id.is_absent:
                                val = {'one_2': False}

                            elif date.day == 12 and not student_id.is_absent:
                                val = {'one_2': True}

                            elif date.day == 13 and student_id.is_absent:
                                val = {'one_3': False}

                            elif date.day == 13 and not student_id.is_absent:
                                val = {'one_3': True}

                            elif date.day == 14 and student_id.is_absent:
                                val = {'one_4': False}

                            elif date.day == 14 and not student_id.is_absent:
                                val = {'one_4': True}

                            elif date.day == 15 and student_id.is_absent:
                                val = {'one_5': False}

                            elif date.day == 15 and not student_id.is_absent:
                                val = {'one_5': True}

                            elif date.day == 16 and student_id.is_absent:
                                val = {'one_6': False}

                            elif date.day == 16 and not student_id.is_absent:
                                val = {'one_6': True}

                            elif date.day == 17 and student_id.is_absent:
                                val = {'one_7': False}

                            elif date.day == 17 and not student_id.is_absent:
                                val = {'one_7': True}

                            elif date.day == 18 and student_id.is_absent:
                                val = {'one_8': False}

                            elif date.day == 18 and not student_id.is_absent:
                                val = {'one_8': True}

                            elif date.day == 19 and student_id.is_absent:
                                val = {'one_9': False}

                            elif date.day == 19 and not student_id.is_absent:
                                val = {'one_9': True}

                            elif date.day == 20 and student_id.is_absent:
                                val = {'one_0': False}

                            elif date.day == 20 and not student_id.is_absent:
                                val = {'one_0': True}

                            elif date.day == 21 and student_id.is_absent:
                                val = {'two_1': False}

                            elif date.day == 21 and not student_id.is_absent:
                                val = {'two_1': True}

                            elif date.day == 22 and student_id.is_absent:
                                val = {'two_2': False}

                            elif date.day == 22 and not student_id.is_absent:
                                val = {'two_2': True}

                            elif date.day == 23 and student_id.is_absent:
                                val = {'two_3': False}

                            elif date.day == 23 and not student_id.is_absent:
                                val = {'two_3': True}

                            elif date.day == 24 and student_id.is_absent:
                                val = {'two_4': False}

                            elif date.day == 24 and not student_id.is_absent:
                                val = {'two_4': True}

                            elif date.day == 25 and student_id.is_absent:
                                val = {'two_5': False}

                            elif date.day == 25 and not student_id.is_absent:
                                val = {'two_5': True}

                            elif date.day == 26 and student_id.is_absent:
                                val = {'two_6': False}

                            elif date.day == 26 and not student_id.is_absent:
                                val = {'two_6': True}

                            elif date.day == 27 and student_id.is_absent:
                                val = {'two_7': False}

                            elif date.day == 27 and not student_id.is_absent:
                                val = {'two_7': True}

                            elif date.day == 28 and student_id.is_absent:
                                val = {'two_8': False}

                            elif date.day == 28 and not student_id.is_absent:
                                val = {'two_8': True}

                            elif date.day == 29 and student_id.is_absent:
                                val = {'two_9': False}

                            elif date.day == 29 and not student_id.is_absent:
                                val = {'two_9': True}

                            elif date.day == 30 and student_id.is_absent:
                                val = {'two_0': False}

                            elif date.day == 30 and not student_id.is_absent:
                                val = {'two_0': True}

                            elif date.day == 31 and student_id.is_absent:
                                val = {'three_1': False}

                            elif date.day == 31 and not student_id.is_absent:
                                val = {'three_1': True}
                            else:
                                val = {}
                            if search_id:
                                search_id.write(val)
                else:
                    for student_id in line.student_ids:
                        search_id = sheet_line_obj. \
                            search([('roll_no', '=', student_id.roll_no),
                                    ('standard_id', '=',
                                     attendance_sheet_id.id)])

                        if date.day == 1 and student_id.is_absent:
                            val = {'one': False}

                        elif date.day == 1 and not student_id.is_absent:
                            val = {'one': True}

                        elif date.day == 2 and student_id.is_absent:
                            val = {'two': False}

                        elif date.day == 2 and not student_id.is_absent:
                            val = {'two': True}

                        elif date.day == 3 and student_id.is_absent:
                            val = {'three': False}

                        elif date.day == 3 and not student_id.is_absent:
                            val = {'three': True}

                        elif date.day == 4 and student_id.is_absent:
                            val = {'four': False}

                        elif date.day == 4 and not student_id.is_absent:
                            val = {'four': True}

                        elif date.day == 5 and student_id.is_absent:
                            val = {'five': False}

                        elif date.day == 5 and not student_id.is_absent:
                            val = {'five': True}

                        elif date.day == 6 and student_id.is_absent:
                            val = {'six': False}

                        elif date.day == 6 and not student_id.is_absent:
                            val = {'six': True}

                        elif date.day == 7 and student_id.is_absent:
                            val = {'seven': False}

                        elif date.day == 7 and not student_id.is_absent:
                            val = {'seven': True}

                        elif date.day == 8 and student_id.is_absent:
                            val = {'eight': False}

                        elif date.day == 8 and not student_id.is_absent:
                            val = {'eight': True}

                        elif date.day == 9 and student_id.is_absent:
                            val = {'nine': False}

                        elif date.day == 9 and not student_id.is_absent:
                            val = {'nine': True}

                        elif date.day == 10 and student_id.is_absent:
                            val = {'ten': False}

                        elif date.day == 10 and not student_id.is_absent:
                            val = {'ten': True}

                        elif date.day == 11 and student_id.is_absent:
                            val = {'one_1': False}

                        elif date.day == 11 and not student_id.is_absent:
                            val = {'one_1': True}

                        elif date.day == 12 and student_id.is_absent:
                            val = {'one_2': False}

                        elif date.day == 12 and not student_id.is_absent:
                            val = {'one_2': True}

                        elif date.day == 13 and student_id.is_absent:
                            val = {'one_3': False}

                        elif date.day == 13 and not student_id.is_absent:
                            val = {'one_3': True}

                        elif date.day == 14 and student_id.is_absent:
                            val = {'one_4': False}

                        elif date.day == 14 and not student_id.is_absent:
                            val = {'one_4': True}

                        elif date.day == 15 and student_id.is_absent:
                            val = {'one_5': False}

                        elif date.day == 15 and not student_id.is_absent:
                            val = {'one_5': True}

                        elif date.day == 16 and student_id.is_absent:
                            val = {'one_6': False}

                        elif date.day == 16 and not student_id.is_absent:
                            val = {'one_6': True}

                        elif date.day == 17 and student_id.is_absent:
                            val = {'one_7': False}

                        elif date.day == 17 and not student_id.is_absent:
                            val = {'one_7': True}

                        elif date.day == 18 and student_id.is_absent:
                            val = {'one_8': False}

                        elif date.day == 18 and not student_id.is_absent:
                            val = {'one_8': True}

                        elif date.day == 19 and student_id.is_absent:
                            val = {'one_9': False}

                        elif date.day == 19 and not student_id.is_absent:
                            val = {'one_9': True}

                        elif date.day == 20 and student_id.is_absent:
                            val = {'one_0': False}

                        elif date.day == 20 and not student_id.is_absent:
                            val = {'one_0': True}

                        elif date.day == 21 and student_id.is_absent:
                            val = {'two_1': False}

                        elif date.day == 21 and not student_id.is_absent:
                            val = {'two_1': True}

                        elif date.day == 22 and student_id.is_absent:
                            val = {'two_2': False}

                        elif date.day == 22 and not student_id.is_absent:
                            val = {'two_2': True}

                        elif date.day == 23 and student_id.is_absent:
                            val = {'two_3': False}

                        elif date.day == 23 and not student_id.is_absent:
                            val = {'two_3': True}

                        elif date.day == 24 and student_id.is_absent:
                            val = {'two_4': False}

                        elif date.day == 24 and not student_id.is_absent:
                            val = {'two_4': True}

                        elif date.day == 25 and student_id.is_absent:
                            val = {'two_5': False}

                        elif date.day == 25 and not student_id.is_absent:
                            val = {'two_5': True}

                        elif date.day == 26 and student_id.is_absent:
                            val = {'two_6': False}

                        elif date.day == 26 and not student_id.is_absent:
                            val = {'two_6': True}

                        elif date.day == 27 and student_id.is_absent:
                            val = {'two_7': False}

                        elif date.day == 27 and not student_id.is_absent:
                            val = {'two_7': True}

                        elif date.day == 28 and student_id.is_absent:
                            val = {'two_8': False}

                        elif date.day == 28 and not student_id.is_absent:
                            val = {'two_8': True}

                        elif date.day == 29 and student_id.is_absent:
                            val = {'two_9': False}

                        elif date.day == 29 and not student_id.is_absent:
                            val = {'two_9': True}

                        elif date.day == 30 and student_id.is_absent:
                            val = {'two_0': False}

                        elif date.day == 30 and not student_id.is_absent:
                            val = {'two_0': True}

                        elif date.day == 31 and student_id.is_absent:
                            val = {'three_1': False}

                        elif date.day == 31 and not student_id.is_absent:
                            val = {'three_1': True}
                        else:
                            val = {}
                        if search_id:
                            search_id.write(val)
        self.state = 'validate'
        return True


# -------------------------------------------------
# Custom Daily Subject Wise Attendance line Class
# -------------------------------------------------
class DailySubjectAttendanceLine(models.Model):
    '''Defining Daily Attendance Sheet Line Information.'''

    _description = 'Daily Subject Attendance Line'
    _name = 'daily.subject.attendance.line'
    _order = 'roll_no'
    _rec_name = 'roll_no'

    roll_no = fields.Integer('Roll No.', help='Roll Number')
    standard_id = fields.Many2one('daily.subject.attendance', 'Standard')
    stud_id = fields.Many2one('student.student', 'Name')
    is_present = fields.Boolean('Present', help="Check if student is present")
    is_absent = fields.Boolean('Absent', help="Check if student is absent")
    present_absentcheck = fields.Boolean('Present/Absent Boolean')

    @api.onchange('is_present')
    def onchange_attendance(self):
        '''Method to make absent false when student is present.'''
        if self.is_present:
            self.is_absent = False
            self.present_absentcheck = True

    @api.onchange('is_absent')
    def onchange_absent(self):
        '''Method to make present false when student is absent.'''
        if self.is_absent:
            self.is_present = False
            self.present_absentcheck = True

    @api.constrains('is_present', 'is_absent')
    def check_present_absent(self):
        '''Method to check present or absent.'''
        for rec in self:
            if not rec.is_present and not rec.is_absent:
                raise ValidationError(_('Check Present or Absent!'))
