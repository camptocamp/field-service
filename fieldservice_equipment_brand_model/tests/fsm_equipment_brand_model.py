# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestFSMEquipmentBrandModel(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Equipment = self.env["fsm.equipment"]
        self.EquipmentBrand = self.env["fsm.equipment.brand"]
        self.EquipmentModel = self.env["fsm.equipment.model"]
        self.equipment = self.Equipment.create({"name": "Equipment"})
        self.equipment_brand = self.EquipmentBrand.create(
            {
                "name": "Equipment Brand",
                "code": "KO",
                "description": "Equipment Brand Description",
            }
        )
        self.equipment_model = self.EquipmentModel.create(
            {
                "name": "Equipment Model",
                "code": "UNI",
                "brand_id": self.equipment_brand.id,
                "description": "Equipment Model Description",
            }
        )

    def test_fsm_equipment_brand_model(self):
        self.equipment.write(
            {
                "brand_id": self.equipment_brand.id,
                "model_brand_id": self.equipment_model.id,
            }
        )
        self.assertEqual(self.equipment_brand, self.equipment.brand_id)
        self.assertEqual(self.equipment_model, self.equipment.model_brand_id)
