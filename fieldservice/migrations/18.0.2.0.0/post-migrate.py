from openupgradelib import openupgrade


def migrate(cr, version):
    """Merge (old) fsm.order.equipment_id into (new) equipment_ids"""
    if not version:
        return
    openupgrade.logged_query(
        cr,
        """
        INSERT INTO fsm_equipment_fsm_order_rel (fsm_order_id, fsm_equipment_id)
        SELECT id AS fsm_order_id, equipment_id
        FROM fsm_order
        WHERE equipment_id IS NOT NULL
        """,
    )
