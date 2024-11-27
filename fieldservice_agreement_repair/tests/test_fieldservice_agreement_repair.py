# Copyright 2024 Camptocamp SA (https://www.camptocamp.com).
# @author: Italo Lopes <italo.lopes@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests.common import TransactionCase


class TestRepairPartSourceLocation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.agreement_model = cls.env["agreement"]
        cls.repair_order_model = cls.env["repair.order"]
        cls.equipment_model = cls.env["fsm.equipment"]
        cls.product_model = cls.env["product.product"]
        cls.lot_model = cls.env["stock.lot"]

        cls.product = cls.product_model.create({"name": "Test Product"})
        cls.product02 = cls.product_model.create({"name": "Test Product 02"})
        cls.product03 = cls.product_model.create({"name": "Test Product 03"})

        cls.lot = cls.lot_model.create({"product_id": cls.product.id})
        cls.lot02 = cls.lot_model.create({"product_id": cls.product02.id})
        cls.lot03 = cls.lot_model.create({"product_id": cls.product03.id})

        cls.agreement = cls.agreement_model.create(
            {
                "name": "Test Agreement",
                "code": "TestAgreement",
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today(),
            }
        )
        cls.agreement02 = cls.agreement_model.create(
            {
                "name": "Test Agreement 02",
                "code": "TestAgreement02",
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today(),
            }
        )

        cls.equipment_with_agreement = cls.equipment_model.create(
            {
                "product_id": cls.product.id,
                "lot_id": cls.lot.id,
                "agreement_id": cls.agreement.id,
            }
        )

        cls.equipment_no_agreement = cls.equipment_model.create(
            {
                "product_id": cls.product02.id,
                "lot_id": cls.lot02.id,
            }
        )
        cls.repair_order = cls.repair_order_model.create(
            {"product_id": cls.product.id, "lot_id": cls.lot.id}
        )

    def test_01_agreement_is_set_correctly(self):
        self.repair_order._compute_agreement_id()
        self.assertEqual(self.repair_order.agreement_id, self.agreement.id)

    def test_02_agreement_is_not_set_when_no_equipment(self):
        repair_order = self.repair_order_model.create(
            {"product_id": self.product03.id, "lot_id": self.lot03.id}
        )
        repair_order._compute_agreement_id()
        self.assertFalse(repair_order.agreement_id)

    def test_03_agreement_is_not_set_when_equipment_no_agreement(self):
        repair_order = self.repair_order_model.create(
            {"product_id": self.product02.id, "lot_id": self.lot02.id}
        )
        equipment = self.equipment_model.search(
            [
                ("product_id", "=", self.product02.id),
                ("lot_id", "=", self.lot02.id),
            ]
        )
        self.assertEqual(equipment, self.equipment_no_agreement)
        repair_order._compute_agreement_id()
        self.assertFalse(repair_order.agreement_id)

    def test_04_agreement_is_not_set_when_no_lot(self):
        product = self.env["product.product"].create({"name": "Test Product"})
        repair_order = self.env["repair.order"].create({"product_id": product.id})
        repair_order._compute_agreement_id()
        self.assertFalse(repair_order.agreement_id)

    def test_05_agreement_is_set_when_lot_updated(self):
        repair_order = self.repair_order_model.create(
            {"product_id": self.product03.id, "lot_id": self.lot03.id}
        )
        repair_order._compute_agreement_id()
        self.assertFalse(repair_order.agreement_id)
        repair_order.product_id = self.product.id
        repair_order.lot_id = self.lot.id
        repair_order._compute_agreement_id()
        self.assertEqual(repair_order.agreement_id, self.agreement.id)

    def test_06_agreement_can_be_updated_manually(self):
        self.repair_order._compute_agreement_id()
        self.assertEqual(self.repair_order.agreement_id, self.agreement.id)
        self.repair_order.agreement_id = self.agreement02.id
        self.assertEqual(self.repair_order.agreement_id, self.agreement02.id)
