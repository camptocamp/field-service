# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class FSMOrder(models.Model):
    _name = "fsm.order"
    _inherit = ["fsm.order", "fsm.equipment.logbook.mixin"]

    def _read_group_logbook_data(self, logbook):
        return logbook.read_group(
            [
                "|",
                ("location_id", "in", self.ids),
                ("equipment_id.location_id", "in", self.ids),
            ],
            ["location_id"],
            ["location_id"],
        )

    def _map_logbook_data(self, logbook, data):
        return {
            db["location_id"][0]: logbook.search(
                [
                    "|",
                    ("location_id", "=", db["location_id"][0]),
                    ("equipment_id.location_id", "=", db["location_id"][0]),
                ]
            )
            for db in data
        }

    def _prepare_equipment_log_vals_list(self):
        order_values = {
            "location_id": self.location_id.id,
            "type": "order",
            "note": self.description or "",
            "res_model": "fsm.order",
        }
        values = self._prepare_log_values()
        values.update(order_values)
        vals_list = []
        if self.type and self.type.name not in ["repair", "maintenance"]:
            if self.equipment_ids:
                for equipment in self.equipment_ids:
                    equipment_values = dict(values)
                    equipment_values.update(
                        {
                            "equipment_status": equipment.stage_id.name,
                            "equipment_id": equipment.id,
                        }
                    )
                    vals_list.append(equipment_values)
        else:
            if self.equipment_id:
                values.update(
                    {
                        "equipment_status": self.equipment_id.stage_id.name,
                        "equipment_id": self.equipment_id.id,
                    }
                )
            vals_list.append(values)
        return vals_list

    def _create_equipment_order_log(self):
        for record in self:
            self.env["fsm.equipment.logbook"].create(
                record._prepare_equipment_log_vals_list()
            )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._create_equipment_order_log()
        return records

    def write(self, vals):
        stage_id = vals.get("stage_id")
        if stage_id:
            user = self.env.user
            closed_orders = self.filtered(lambda l: l.stage_id.is_closed)  # noqa: E741
            if not user.has_group("fieldservice.group_fsm_manager") and closed_orders:
                raise ValidationError(
                    _(
                        "The FSM Order has been closed, "
                        "you are not permitted to changes it's stage."
                    )
                )
        res = super().write(vals)
        if stage_id:
            self._create_equipment_order_log()
        return res
