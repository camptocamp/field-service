# Copyright 2024 Camptocamp SA (https://www.camptocamp.com).
# @author: Italo Lopes <italo.lopes@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for order in res:
            if order.repair_id and order.agreement_id:
                order.repair_id.agreement_id = order.agreement_id.id
        return res
