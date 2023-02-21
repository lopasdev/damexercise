# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _name = 'market.product.category'

    _parent_store = True
    _parent_name = "parent_id"  # optional if field is 'parent_id'

    name = fields.Char('Category')
    description = fields.Text('Description')
    parent_id = fields.Many2one(
        'market.product.category',
        string='Parent Category',
        ondelete='restrict',
        index=True
    )
    products_ids = fields.One2many(
        'market.product.category', 'parent_id',
        string='Product Categories')
    parent_path = fields.Char(index=True)

    product_ids = fields.One2many('market.product', 'category_id', 'products')

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')