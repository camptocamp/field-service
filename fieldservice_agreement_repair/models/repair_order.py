# Copyright 2024 Camptocamp SA (https://www.camptocamp.com).
# @author: Italo Lopes <italo.lopes@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FSMEquipment(models.Model):
    _inherit = "repair.order"

    agreement_id = fields.Many2one(
        "agreement", compute="_compute_agreement_id", store=True, readonly=False
    )

    @api.depends("product_id", "lot_id", "lot_id.product_id")
    def _compute_agreement_id(self):
        for repair in self:
            if repair.product_id and repair.lot_id:
                equipment_id = self.env["fsm.equipment"].search(
                    [
                        ("product_id", "=", repair.product_id.id),
                        ("lot_id", "=", repair.lot_id.id),
                    ]
                )
                if equipment_id and equipment_id.agreement_id:
                    repair.agreement_id = equipment_id.agreement_id.id
