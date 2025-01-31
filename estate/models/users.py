from odoo import fields, models
#from dateutil.relativedelta import relativedelta


class Users(models.Model):
    _inherit = "res.users"

    property_id = fields.One2many("estate.property", "salesperson", string="Salesperson",  domain=['|', ('state', '=', 'new'), ('state', '=', 'offer received')])