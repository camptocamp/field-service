# Copyright (C) 2019 Clément Mombereau (Akretion)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo.tests.common import TransactionCase


class FSMSale(TransactionCase):
    @classmethod
    def setUpClass(cls):
        """Create 3 related partners : a parent company, a child partner and
        a child shipping partner.

        For each test, a different partner is a fsm_location.
        A SO is created with the child partner as customer. The test run
        the SO's location autofill and check if the fsm_location_id
        is the expected one.
        """
        super().setUpClass()
        # create a parent company
        cls.commercial_partner = cls.env["res.partner"].create(
            {"name": "Company Commercial Partner", "is_company": True}
        )
        # create a child partner
        cls.partner1 = cls.env["res.partner"].create(
            {"name": "Child Partner 1", "parent_id": cls.commercial_partner.id}
        )
        cls.partner2 = cls.env["res.partner"].create(
            {"name": "Child Partner 2", "parent_id": cls.commercial_partner.id}
        )
        # create a child partner shipping address
        cls.shipping_partner = cls.env["res.partner"].create(
            {
                "name": "Shipping Partner",
                "parent_id": cls.commercial_partner.id,
                "type": "delivery",
            }
        )
        # Demo FS location
        cls.location = cls.env.ref("fieldservice.location_1")
        cls.partner2.fsm_location = cls.location

    def test_00_autofill_so_fsm_location(self):
        """First case :
        - commercial_partner IS NOT a fsm_location
        - partner IS a fsm_location
        - shipping_partner IS NOT a fsm_location
        Test if the SO's fsm_location_id is autofilled with the expected
        partner_location.
        """
        # Link demo FS location to self.partner1
        self.location.partner_id = self.partner1
        self.so = self.env["sale.order"].create({"partner_id": self.partner2.id})
        self.assertEqual(self.so.fsm_location_id, self.location)

    def test_01_autofill_so_fsm_location(self):
        """First case :
        - commercial_partner IS NOT a fsm_location
        - partner IS a fsm_location
        - shipping_partner IS NOT a fsm_location
        Test if the SO's fsm_location_id is autofilled with the expected
        partner_location.
        """
        # Link demo FS location to self.partner
        self.location.partner_id = self.partner1
        self.so = self.env["sale.order"].create({"partner_id": self.partner1.id})
        self.assertEqual(self.so.fsm_location_id, self.location)

    def test_02_autofill_so_fsm_location(self):
        """Second case :
        - commercial_partner IS NOT a fsm_location
        - partner IS NOT a fsm_location
        - shipping_partner IS a fsm_location
        Test if the SO's fsm_location_id is autofilled with the expected
        shipping_partner_location.
        """
        # Link demo FS location to self.shipping_partner
        self.location.partner_id = self.shipping_partner.id
        self.so = self.env["sale.order"].create({"partner_id": self.partner1.id})
        self.assertEqual(self.so.fsm_location_id, self.location)

    def test_03_autofill_so_fsm_location(self):
        """Third case :
        - commercial_partner IS a fsm_location
        - partner IS NOT a fsm_location
        - shipping_partner IS NOT a fsm_location
        Test if the SO's fsm_location_id is autofilled with the expected
        commercial_partner_location.
        """
        # Link demo FS location to self.commercial_partner
        self.location.partner_id = self.commercial_partner
        self.so = self.env["sale.order"].create({"partner_id": self.partner1.id})
        self.assertEqual(self.so.fsm_location_id, self.location)
