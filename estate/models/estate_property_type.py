# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
#from dateutil.relativedelta import relativedelta


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name"
    
    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_id = fields.One2many("estate.property", "property_type_id", string="Property ID", required=True)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_count_offers")

    @api.depends('offer_ids')
    def _compute_count_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    
    _sql_constraints = [
        ('check_type_name', 'unique(name)',
         'Type already exists')
    ]

