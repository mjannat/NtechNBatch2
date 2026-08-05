from odoo import api, fields, models
from odoo.exceptions import ValidationError


class QualityCheckLine(models.Model):
    _name = "quality.check.line"
    _description = "Quality Control Check Line"

    product_id = fields.Many2one('product.product', 'Product', required=True)
    rec_qty = fields.Float('Receive Qty', required=True)
    damage_qty = fields.Float('Damage Qty', required=True)
    remain_qty = fields.Float('Remain Qty', required=True)
    line_id = fields.Many2one('quality.check', 'Line', required=True)