from odoo import fields, models
#from dateutil.relativedelta import relativedelta


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(required=True)
