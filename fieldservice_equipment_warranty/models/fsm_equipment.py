# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class FSMEquipment(models.Model):
    _inherit = "fsm.equipment"

    warranty_start_date = fields.Date(
        copy=False, tracking=True, default=fields.Date.today
    )
    warranty_end_date = fields.Date(
        copy=False, tracking=True, default=fields.Date.today
    )
    product_warranty = fields.Integer(
        related="product_id.warranty", string="Warranty Duration"
    )
    product_warranty_type = fields.Selection(
        related="product_id.warranty_type", string="Warranty Type"
    )

    def _get_warranty_end_date(self):
        self.ensure_one()
        warranty_end_date = fields.Date.today()
        if self.product_id and self.product_id.warranty:
            if self.product_id.warranty_type == "week":
                warranty_end_date = self.warranty_start_date + relativedelta(
                    weeks=self.product_id.warranty
                )
            elif self.product_id.warranty_type == "month":
                warranty_end_date = self.warranty_start_date + relativedelta(
                    months=self.product_id.warranty
                )
            elif self.product_id.warranty_type == "year":
                warranty_end_date = self.warranty_start_date + relativedelta(
                    years=self.product_id.warranty
                )
            else:
                warranty_end_date = fields.Date.today() + relativedelta(
                    days=self.product_id.warranty
                )
        return warranty_end_date

    @api.onchange("product_id", "product_id.warranty", "warranty_start_date")
    def _onchange_product_warranty(self):
        self.warranty_end_date = self._get_warranty_end_date()

    def write(self, vals):
        res = super().write(vals)
        if "product_id" in vals or "warranty_start_date" in vals:
            for equip in self:
                warranty_end_date = equip._get_warranty_end_date()
                equip.warranty_end_date = warranty_end_date
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for equip in res:
            warranty_end_date = equip._get_warranty_end_date()
            equip.warranty_end_date = warranty_end_date
        return res
