# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api,fields,models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', index=True, copy=False, readonly=True)
    description = fields.Text()
    postcode = fields.Char()
    property_type_id = fields.Many2one("estate.property.type")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute="_compute_best_price")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    sell_accepted = fields.Boolean(default = False)
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Integer(compute="_compute_total_area")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="This gives you garden orientation")
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new','New'), ('offer received','Offer Received'), ('offer accepted','Offer Accepted'), ('sold','Sold'), ('canceled','Canceled')],
        default = 'new',
        required = True,
        copy = False,
        help="Offer Status")
    
    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for line in self:
            if line.offer_ids.mapped('price'):
                line.best_price = max(line.offer_ids.mapped('price'))
            else:
                line.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == False:
            self.garden_area = 0
            self.garden_orientation = ''
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'
    
    def sell_property(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled properties cannot be sold")
            else:
                record.state = "sold"

    def cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled")
            else:
                record.state = "canceled"
    