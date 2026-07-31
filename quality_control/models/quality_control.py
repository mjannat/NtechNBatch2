from odoo import api, fields, models


class QualityControl(models.Model):
    _name = "quality.control"
    _description = "Inventory Customization For QC"

    code = fields.Char(string="Code", required=True)
    final_approve_user_id = fields.Many2one('res.users', "Final Approver", required=False)
    qc_state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("approved", "Approved"),
            ("partially_approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        string="QC State",
        default="draft",
    )
    remarks = fields.Text(string="Remarks")
    line_ids = fields.One2many('quality.control.line', "qc_id", string="QC Lines")
    additional_inspector_ids = fields.Many2many(
        comodel_name='res.users',
        relation='quality_check_res_users_rel',
        column1='check_id',
        column2='user_id',
        string='Additional Inspectors'
    )




