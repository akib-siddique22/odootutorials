# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
#from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

class EstateProperty(models.Model):
    _inherit="estate.property"

    def sell_property(self):
        
        for property in self:
            self.env['account.move'].create({
                'partner_id': property.buyer.id,  
                'move_type': 'out_invoice', 
                "invoice_line_ids": [
                    (0, 0, {
                        'name': f'Commission for {property.name}',
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    (0, 0, {
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ]
            })
        
        return super().sell_property()