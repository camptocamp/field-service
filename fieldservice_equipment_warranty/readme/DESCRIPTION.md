Customizations related to ``fieldservice_equipment_stock`` module and ``product_warranty`` module.

Models:

* On ``fsm.equipment`` model:
   * Add two new fields ``warranty_start_date`` and ``warranty_end_date``.
   * Override ``create`` method to set the ``warranty_end_date`` field based on warranty duration.

Views:

* On ``fieldservice_equipment_stock.fsm_equipment_form_view_stock`` form view:
   * Add both field into list/form view.
