# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    @api.model
    def create(self, vals):
        res = super(FSMOrder, self).create(vals)
        action = self.env["fsm.stage"].browse(vals.get("stage_id")).action_id
        if action:
            context = {
                "active_model": self._name,
                "active_ids": [res.id],
            }
            action.with_context(**context).run()
        return res

    def write(self, vals):
        res = super().write(vals)
        action = self.env["fsm.stage"].browse(vals.get("stage_id")).action_id
        if action:
            context = {
                "active_model": self._name,
                "active_ids": self.ids,
            }
            action.with_context(**context).run()
        return res
