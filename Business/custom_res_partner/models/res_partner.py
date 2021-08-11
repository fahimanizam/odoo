# -*- coding: utf-8 -*-
from pytz import timezone
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


# Custom Product Template
class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def _default_interest(self):
        return self.env['res.partner.interest'].browse(self._context.get('interest_id'))

    def _default_food(self):
        return self.env['res.partner.fav.food'].browse(self._context.get('fav_food'))

    def _default_available_food(self):
        return self.env['restaurant.food'].browse(self._context.get('available_food'))

    time = fields.Char(string='Opening Time')

    interest_id = fields.Many2many('res.partner.interest',
                                   column1='partner_id',
                                   column2='interest_id',
                                   string='Interests',
                                   default=_default_interest)
    fav_food = fields.Many2many('res.partner.fav.food',
                                column1='partner_id',
                                column2='fav_food',
                                string='Favorite Food',
                                default=_default_food)
    available_food = fields.Many2many('restaurant.food',
                                      column1='partner_id',
                                      column2='available_food',
                                      string='Favorite Food',
                                      default=_default_available_food)

    usertype = fields.Selection([
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
    ], 'User Type', default='customer', required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], 'Gender', default='male')
    relationship = fields.Selection([
        ('single', 'Single'),
        ('engaged', 'Engaged'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
    ], 'Status', default='single')

    # age = fields.Text('Message for Sales Order')
    birthday = fields.Date(string="DOB")

    age = fields.Integer(string="Age")

    @api.onchange('birthday')
    def _onchange_birth_date(self):
        if self.birthday:
            d1 = datetime.strptime(str(self.birthday), "%Y-%m-%d").date()
            d2 = date.today()
            self.age = relativedelta(d2, d1).years

    user_event_count = fields.Integer(
        'Events', compute='_compute_user_event_count', groups='event.group_event_user',
        help='Number of events created by user')

    def _compute_user_event_count(self):
        self.user_event_count = 0
        if not self.user_has_groups('event.group_event_user'):
            return
        for partner in self:
            partner.user_event_count = self.env['event.event'].search_count(
                [('user_id', '=', partner.id)])

    def action_user_event_view(self):
        action = self.env["ir.actions.actions"]._for_xml_id("custom_res_partner.action_user_event_view")
        action['context'] = {}
        action['domain'] = [('user_id', '=', self.id)]
        return action


class ResPartnerInterest(models.Model):
    _description = 'Partner Interests'
    _name = "res.partner.interest"
    _order = 'name'
    _parent_store = True

    name = fields.Char(string='Interest Name',
                       required=True,
                       translate=True)
    color = fields.Integer(string='Color Index')
    parent_id = fields.Many2one('res.partner.interest',
                                string='Parent Interest',
                                index=True,
                                ondelete='cascade')
    child_ids = fields.One2many('res.partner.interest', 'parent_id',
                                string='Child Interests')
    active = fields.Boolean(default=True,
                            help="The active field allows you to hide the interest without removing it.")
    parent_path = fields.Char(index=True)
    partner_ids = fields.Many2many('res.partner',
                                   column1='interest_id',
                                   column2='partner_id',
                                   string='Partners')

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You can not create recursive interests.'))

    def name_get(self):
        if self._context.get('partner_interest_display') == 'short':
            return super(ResPartnerInterest, self).name_get()

        res = []
        for interest in self:
            names = []
            current = interest
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((interest.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
        # return models.lazy_name_get(self.browse(partner_interest_ids).with_user(name_get_uid))


class ResPartnerFavFood(models.Model):
    _description = 'Partner Favorite'
    _name = "res.partner.fav.food"
    _order = 'name'
    _parent_store = True

    name = fields.Char(string='Favorite Food Name',
                       required=True,
                       translate=True)
    color = fields.Integer(string='Color Index')
    parent_id = fields.Many2one('res.partner.fav.food',
                                string='Parent Favorite Food',
                                index=True,
                                ondelete='cascade')
    child_ids = fields.One2many('res.partner.fav.food', 'parent_id',
                                string='Child Favorite Food')
    active = fields.Boolean(default=True,
                            help="The active field allows you to hide the favorite food without removing it.")
    parent_path = fields.Char(index=True)
    partner_ids = fields.Many2many('res.partner',
                                   column1='fav_food',
                                   column2='partner_id',
                                   string='Partners')

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You can not create recursive food.'))

    def name_get(self):
        if self._context.get('partner_fav_food_display') == 'short':
            return super(ResPartnerFavFood, self).name_get()

        res = []
        for food in self:
            names = []
            current = food
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((food.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
        # return models.lazy_name_get(self.browse(partner_fav_food_ids).with_user(name_get_uid))


class RestaurantFood(models.Model):
    _description = 'Restaurant food'
    _name = "restaurant.food"
    _order = 'name'
    _parent_store = True

    name = fields.Char(string='Available Food',
                       required=True,
                       translate=True)
    color = fields.Integer(string='Color Index')
    parent_id = fields.Many2one('restaurant.food',
                                string='Parent Food',
                                index=True,
                                ondelete='cascade')
    child_ids = fields.One2many('restaurant.food', 'parent_id',
                                string='Child Food')
    active = fields.Boolean(default=True,
                            help="The active field allows you to hide the Food without removing it.")
    parent_path = fields.Char(index=True)
    partner_ids = fields.Many2many('res.partner',
                                   column1='available_food',
                                   column2='partner_id',
                                   string='Partners')

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You can not create recursive food.'))

    def name_get(self):
        if self._context.get('partner_fav_food_display') == 'short':
            return super(RestaurantFood, self).name_get()

        res = []
        for food in self:
            names = []
            current = food
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((food.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)


class CustomEventEvent(models.Model):
    _inherit = 'event.event'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        default=lambda self: self.env.user)


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    partner_id = fields.Many2one(
        'res.partner', string='Booked by', tracking=True, default=lambda self: self.env.user,
        states={'done': [('readonly', True)]})

    _sql_constraints = [
        ('event_registration_unique', 'unique(partner_id,event_id)',
         'This id is registered already!')
    ]
