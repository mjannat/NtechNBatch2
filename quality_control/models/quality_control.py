# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api, fields, models
from odoo.exceptions import ValidationError

RESULT = [
    ("pass", "Pass"),
    ("fail", "Fail"),
],

STATE = [
    ('draft', 'Draft'),
    ('manager', 'Manager'),
    ('supervisor', 'Supervisor'),
    ('approved', 'Approved'),
    ('cancel', 'Cancel'),

]


class QualityCheck(models.Model):
    _name = "quality.check"
    _description = "Quality Control Check"
    _rec_name = "name"

    # ==========================================
    # FIELD DEFINITIONS
    # ==========================================
    name = fields.Char(
        string="Reference",
        required=False,
        copy=False,
        readonly=False,
        default="New",
    )
    inspector_id = fields.Many2one("res.users", "Main Checker", required="True",
                                   readonly=True, store=True, default=lambda self: self.env.user)
    quantity_lines = fields.One2many("quality.check.line", "line_id", string="Product Lines")
    additional_inspector_ids = fields.Many2many(
        comodel_name="res.users",
        string="Additional Inspectors",
    )
    check_date = fields.Date(
        string="Check Date",
        default=fields.Date.today,
    )
    remarks = fields.Text(
        string="Remarks",
    )
    result = fields.Selection(
        selection=RESULT,
        string="Result",
        tracking=True,
    )
    state = fields.Selection(
        selection=STATE,
        string="Status",
        default="draft",
        tracking=True,
    )

    is_field_readonly = fields.Boolean(string="Is Field Readonly", default=False,
                                       compute="_compute_is_field_readonly")

    @api.depends('state')
    def _compute_is_field_readonly(self):
        for rec in self:
            rec.is_field_readonly = rec.state in ['manager', 'supervisor', 'approved', 'cancel']

    # quantity_lines = fields.One2many('quality.check.line', 'line_id','Product Line')
    #
    # # ==========================================
    # # ORM OVERRIDES
    # # # ==========================================
    # # @api.model
    # # def create(self, vals_list):
    # #     """Generates sequence reference number on creation."""
    # #     for vals in vals_list:
    # #         if vals.get("name", "New") == "New":
    # #             seq_code = "quality.check.code"
    # #             vals["name"] = self.env["ir.sequence"].next_by_code(seq_code) or "New"
    # #     return super(QualityCheck, self).create(vals_list)

    # ==========================================
    # BUSINESS ACTIONS
    # ==========================================
    def action_send_to_manager(self):
        """Moves the state to confirmed."""
        if self.state == 'draft':
            self.state = 'manager'

    def action_send_to_supervisor(self):
        """Moves the state to confirmed."""
        if self.state == 'manager':
            self.state = 'supervisor'

    def action_cancel(self):
        self.state = 'cancel'

    def action_approved(self):
        """Validates result and sets state to done."""
        self.state = 'approved'
        self.result = 'pass'

    @api.onchange("inspector_id")
    def _onchange_inspector_id(self):
        if self.inspector_id:
            self.additional_inspector_ids = [(6, 0, [self.inspector_id.id])]
            self.remarks = "The main inspector is: %s" % self.inspector_id.name

    @api.ondelete(at_uninstall=False)
    def _ondelete_check(self):
        """Prevents deletion of quality check lines if the parent quality check is not in draft state."""
        for rec in self:
            if rec.state != "draft":
                raise ValidationError(
                    "You can only delete QC it is in draft state."
                )
