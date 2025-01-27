# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
#from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from . import estate_property


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()
    create_date = fields.Datetime(default=fields.Datetime.now)
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help="Offer Decision",
        copy = False)
    validity = fields.Integer(default=7, inverse="_inverse_deadline", string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_deadline", string="Deadline")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property ID", required=True)

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for line in self:
            line.date_deadline = line.create_date.date() + timedelta(days=line.validity)
    
    @api.depends('create_date', 'date_deadline')
    def _inverse_deadline(self):
        for line in self:
            line.validity = (line.date_deadline - line.create_date.date()).days

    def action_accept(self):
        for record in self:
            if self.property_id.sell_accepted == False:
                self.property_id.sell_accepted = True
                self.property_id.selling_price = self.price
                self.property_id.buyer = self.partner_id.id
                record.status = 'accepted'

    def action_reject(self):
        for record in self:
            if self.status == 'accepted':
                self.property_id.sell_accepted = False
                self.property_id.selling_price = 0
                self.property_id.buyer = None
                record.status = 'refused'
            else:
                record.status = 'refused'

    _sql_constraints = [  
        ('check_offer_price', 'CHECK(price > 0)',
         'Expected price must be strictly positive')
    ]