from odoo import fields, models
#from dateutil.relativedelta import relativedelta


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('check_tag_name', 'unique(name)',
         'Tag already exists')
    ]
