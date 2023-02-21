# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

logger = logging.getLogger(__name__)


class MarketLopan(models.Model):
    _name = 'market.lopan'
    _description = 'market lopan'

    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner', string='Proveedor')
    category_id = fields.Many2one('market.lopan.category', string='Category')

    state = fields.Selection([
        ('fresh', 'Fresh'),
        ('timedOut', 'TimedOut'),
        ('retired', 'Retired')],
        'State', default="fresh")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('fresh', 'timedOut'),
                   ('timedOut', 'retired'),
                   ('retired', 'fresh'),]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for lopan in self:
            if lopan.is_allowed_transition(lopan.state, new_state):
                lopan.state = new_state
            else:
                message = _('Moving from %s to %s is not allowd') % (lopan.state, new_state)
                raise UserError(message)

    def make_fresh(self):
        self.change_state('fresh')

    def make_timedOut(self):
        self.change_state('timedOut')

    def make_retired(self):
        self.change_state('retired')

    def log_all_market_members(self):
        market_member_model = self.env['market.member']  # This is an empty recordset of model market.member
        all_members = market_member_model.search([])
        print("ALL MEMBERS:", all_members)
        return True


    def create_categories(self):
        categ1 = {
            'name': 'corta',
            'description': 'Caducidad corta'
        }
        categ2 = {
            'name': 'media',
            'description': 'Caducidad media'
        }
        categ3 = {
            'name': 'larga',
            'description': 'Caducidad larga'
        }
        parent_category_val = {
            'name': 'Parent category',
            'description': 'Description for parent category',
            'product_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
                (0, 0, categ3),
            ]
        }
        # Total 3 records (1 parent and 2 product) will be craeted in market.lopan.category model
        record = self.env['market.lopan.category'].create(parent_category_val)
        return True

    def change_release_date(self):
        self.ensure_one()
        self.date_release = fields.Date.today()

    def find_lopan(self):
        domain = [
            '|',
                '&', ('name', 'ilike', 'lopan Name'),
                     ('category_id.name', '=', 'Category Name'),
                '&', ('name', 'ilike', 'lopan Name 2'),
                     ('category_id.name', '=', 'Category Name 2')
        ]
        lopans = self.search(domain)
        logger.info('lopans found: %s', lopans)
        return True

class marketMember(models.Model):

    _name = 'market.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = "market member"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')

class ResPartner(models.Model):
    _inherit = 'res.partner'

    authored_lopan_ids = fields.Many2many(
        'market.lopan',
        string='Authored lopans',
        # relation='market_lopan_res_partner_rel'  # optional
    )