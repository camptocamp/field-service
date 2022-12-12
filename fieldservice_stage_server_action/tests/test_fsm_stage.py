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
        # Equipment
        self.server_action_equipment = self.ServerAction.create(
            {
                "name": "Equipment Server Action",
                "model_id": self.env.ref("fieldservice.model_fsm_equipment").id,
                "state": "multi",
            }
        )
        self.env["fsm.stage"].search([]).unlink()
        self.stage_equipment_1 = self.FSMStage.create(
            {
                "name": "Equipment Stage 1",
                "stage_type": "equipment",
                "action_id": self.server_action_equipment.id,
                "sequence": 1,
            }
        )
        self.stage_equipment_2 = self.FSMStage.create(
            {
                "name": "Location Stage 2",
                "stage_type": "equipment",
                "action_id": self.server_action_equipment.id,
                "sequence": 2,
            }
        )
        # Location
        self.server_action_location = self.ServerAction.create(
            {
                "name": "Location Server Action",
                "model_id": self.env.ref("fieldservice.model_fsm_location").id,
                "state": "multi",
            }
        )
        self.stage_location_1 = self.FSMStage.create(
            {
                "name": "Location Stage 1",
                "stage_type": "location",
                "action_id": self.server_action_location.id,
                "sequence": 1,
            }
        )
        self.stage_location_2 = self.FSMStage.create(
            {
                "name": "Location Stage 2",
                "stage_type": "location",
                "action_id": self.server_action_location.id,
                "sequence": 2,
            }
        )
        # Order
        self.server_action_order = self.ServerAction.create(
            {
                "name": "Order Server Action",
                "model_id": self.env.ref("fieldservice.model_fsm_order").id,
                "state": "multi",
            }
        )
        self.stage_order_1 = self.FSMStage.create(
            {
                "name": "Order Stage 1",
                "stage_type": "order",
                "action_id": self.server_action_order.id,
                "sequence": 1,
            }
        )
        self.stage_order_2 = self.FSMStage.create(
            {
                "name": "Order Stage 2",
                "stage_type": "order",
                "action_id": self.server_action_order.id,
                "sequence": 2,
            }
        )
        # Worker
        self.server_action_worker = self.ServerAction.create(
            {
                "name": "Worker Server Action",
                "model_id": self.env.ref("fieldservice.model_fsm_order").id,
                "state": "multi",
            }
        )
        self.stage_worker_1 = self.FSMStage.create(
            {
                "name": "Worker Stage 1",
                "stage_type": "worker",
                "action_id": self.server_action_worker.id,
                "sequence": 1,
            }
        )
        self.stage_worker_2 = self.FSMStage.create(
            {
                "name": "Worker Stage 2",
                "stage_type": "worker",
                "action_id": self.server_action_worker.id,
                "sequence": 2,
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
        # Create
        self.worker = self.FSMPerson.create(
            {"name": "Worker", "stage_id": self.stage_worker_1.id}
        )
        self.assertEqual(len(self.worker.activity_ids), 1)
        # Write
        self.worker.write({"stage_id": self.stage_worker_2.id})
        self.assertEqual(len(self.worker.activity_ids), 2)
