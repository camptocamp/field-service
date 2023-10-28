# Copyright (C) 2019 Brian McMaster
# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    fsm_recurring_id = fields.Many2one(
        "fsm.recurring",
        "Recurring Order",
        index=True,
        help="Field Service Recurring Order generated by the sale order line",
    )

    def _field_create_fsm_recurring_prepare_values(self):
        self.ensure_one()
        template = self.product_id.fsm_recurring_template_id
        product = self.product_id
        note = self.name
        if template.description:
            note += "\n " + template.description
        return {
            "location_id": self.order_id.fsm_location_id.id,
            "start_date": self.order_id.expected_date,
            "fsm_recurring_template_id": template.id,
            "description": note,
            "max_orders": template.max_orders,
            "fsm_frequency_set_id": template.fsm_frequency_set_id.id,
            "fsm_order_template_id": product.fsm_order_template_id.id
            or template.fsm_order_template_id.id,
            "sale_line_id": self.id,
            "company_id": self.company_id.id,
        }

    def _field_create_fsm_recurring(self):
        """Generate fsm_recurring for the given so line, and link it.
        :return a mapping with the so line id and its linked fsm_recurring
        :rtype dict
        """
        result = {}
        for so_line in self:
            # create fsm_recurring
            values = so_line._field_create_fsm_recurring_prepare_values()
            fsm_recurring = self.env["fsm.recurring"].sudo().create(values)
            fsm_recurring.action_start()
            so_line.write({"fsm_recurring_id": fsm_recurring.id})
            # post message on SO
            msg_body = _(
                """Field Service recurring Created (%(product)s): <a href=
                   # data-oe-model=fsm.recurring data-oe-id=%(id)s>%(name)s</a>
                """
            ).format(
                {
                    "product": so_line.product_id.name,
                    "id": fsm_recurring.id,
                    "name": fsm_recurring.name,
                }
            )
            so_line.order_id.message_post(body=msg_body)
            # post message on fsm_recurring
            fsm_recurring_msg = _(
                """This recurring has been created from: <a href=
                   # data-oe-model=sale.order data-oe-id=%(order_id)s>%(order)s</a>
                   (%(product)s)
                """
            ).format(
                {
                    "order_id": so_line.order_id.id,
                    "order": so_line.order_id.name,
                    "product": so_line.product_id.name,
                }
            )
            fsm_recurring.message_post(body=fsm_recurring_msg)
            result[so_line.id] = fsm_recurring
        return result
