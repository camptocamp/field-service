# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class FSMRecurringCase(TransactionCase):
    def setUp(self):
        super(FSMRecurringCase, self).setUp()
        self.FSMEquipment = self.env["fsm.equipment"]
        self.FSMLocation = self.env["fsm.location"]
        self.FSMOrders = self.env["fsm.order"]
        self.FSMPerson = self.env["fsm.person"]
        self.FSMStage = self.env["fsm.stage"]
        self.ServerAction = self.env["ir.actions.server"]
        # Mail Activity Type
        self.activity_type = self.env["mail.activity.type"].create({"name": "To Do"})
        # Phone Number
        self.phone = "070-070-070"
        # Equipment
        self.server_action_equipment = self.ServerAction.create(
            {
                "name": "Equipment Server Action",
                "model_id": self.env.ref("fieldservice.model_fsm_equipment").id,
                "state": "next_activity",
                "activity_user_field_name": "user_id",
                "activity_type_id": self.activity_type.id,
                "activity_user_type": "generic",
            }
        )
        self.stage_equipment_1 = self.FSMStage.create(
            {
                "name": "Equipment Stage 1",
                "stage_type": "equipment",
                "action_id": self.server_action_equipment.id,
                "sequence": 10,
            }
        )
        self.stage_equipment_2 = self.FSMStage.create(
            {
                "name": "Equipment Stage 2",
                "stage_type": "equipment",
                "action_id": self.server_action_equipment.id,
                "sequence": 11,
            }
        )
        # Location
        self.server_action_location = self.ServerAction.create(
            {
                "name": "Location Server Action",
                "model_id": self.env.ref("fieldservice.model_fsm_location").id,
                "state": "next_activity",
                "activity_user_field_name": "user_id",
                "activity_type_id": self.activity_type.id,
                "activity_user_type": "generic",
            }
        )
        self.stage_location_1 = self.FSMStage.create(
            {
                "name": "Location Stage 1",
                "stage_type": "location",
                "action_id": self.server_action_location.id,
                "sequence": 12,
            }
        )
        self.stage_location_2 = self.FSMStage.create(
            {
                "name": "Location Stage 2",
                "stage_type": "location",
                "action_id": self.server_action_location.id,
                "sequence": 13,
            }
        )
        # Order
        self.server_action_order = self.ServerAction.create(
            {
                "name": "Order Server Action",
                "model_id": self.env.ref("fieldservice.model_fsm_order").id,
                "state": "next_activity",
                "activity_user_field_name": "user_id",
                "activity_type_id": self.activity_type.id,
                "activity_user_type": "generic",
            }
        )
        self.stage_order_1 = self.FSMStage.create(
            {
                "name": "Order Stage 1",
                "stage_type": "order",
                "action_id": self.server_action_order.id,
                "sequence": 14,
            }
        )
        self.stage_order_2 = self.FSMStage.create(
            {
                "name": "Order Stage 2",
                "stage_type": "order",
                "action_id": self.server_action_order.id,
                "sequence": 15,
            }
        )
        # Worker
        self.field = self.env["ir.model.fields"]._get(self.FSMPerson._name, "phone")
        self.server_action_worker = self.ServerAction.create(
            {
                "name": "Worker Server Action",
                "model_id": self.env.ref("fieldservice.model_fsm_person").id,
                "state": "object_write",
                "fields_lines": [
                    (
                        0,
                        0,
                        {
                            "col1": self.field.id,
                            "evaluation_type": "value",
                            "value": self.phone,
                        },
                    )
                ],
            }
        )
        self.stage_worker_1 = self.FSMStage.create(
            {
                "name": "Worker Stage 1",
                "stage_type": "worker",
                "action_id": self.server_action_worker.id,
                "sequence": 16,
            }
        )
        self.stage_worker_2 = self.FSMStage.create(
            {
                "name": "Worker Stage 2",
                "stage_type": "worker",
                "action_id": self.server_action_worker.id,
                "sequence": 17,
            }
        )

    def test_fsm_equipment(self):
        # Create
        self.equipment = self.FSMEquipment.create(
            {"name": "Equipment", "stage_id": self.stage_equipment_1.id}
        )
        self.assertEqual(len(self.equipment.activity_ids), 1)
        # Write
        self.equipment.write({"stage_id": self.stage_equipment_2.id})
        self.assertEqual(len(self.equipment.activity_ids), 2)

    def test_fsm_location(self):
        # Create
        self.worker = self.FSMPerson.create({"name": "Worker"})
        self.location = self.FSMLocation.create(
            {
                "name": "Location",
                "stage_id": self.stage_location_1.id,
                "owner_id": self.worker.id,
            }
        )
        self.assertEqual(len(self.location.activity_ids), 1)
        # Write
        self.location.write({"stage_id": self.stage_location_2.id})
        self.assertEqual(len(self.location.activity_ids), 2)

    def test_fsm_order(self):
        # Create
        self.worker = self.FSMPerson.create({"name": "Worker"})
        self.location = self.FSMLocation.create(
            {"name": "Location", "owner_id": self.worker.id}
        )
        self.order = self.FSMOrders.create(
            {
                "name": "Order",
                "stage_id": self.stage_order_1.id,
                "location_id": self.location.id,
            }
        )
        self.assertEqual(len(self.order.activity_ids), 1)
        # Write
        self.order.write({"stage_id": self.stage_order_2.id})
        self.assertEqual(len(self.order.activity_ids), 2)

    def test_fsm_worker(self):
        self.worker = self.FSMPerson.create(
            {"name": "Worker", "stage_id": self.stage_worker_1.id}
        )
        self.assertEqual(self.worker.phone, self.phone)
        self.worker.write({"phone": False})
        self.worker.write({"stage_id": self.stage_worker_2.id})
        self.assertEqual(self.worker.phone, self.phone)
