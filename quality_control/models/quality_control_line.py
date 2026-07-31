from odoo import api, fields, models


class QualityControlLine(models.Model):
    _name = "quality.control.line"
    _description = "Inventory Customization For QC Product Line"

    product_id = fields.Many2one("product.product", required=True)
    purchase_qty = fields.Float("Purchase Qty", required=True)
    product_qty = fields.Float("Quantity", required=True)
    qc_id = fields.Many2one("quality.control", string="QC Reference", required=True)