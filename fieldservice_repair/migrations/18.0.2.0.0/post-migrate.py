from openupgradelib import openupgrade


def migrate(cr, version):
    """Merge (old) fsm.order.repair_id into (new) repair_ids"""
    if not version:
        return
    openupgrade.logged_query(
        cr,
        """
        UPDATE repair_order
        SET fsm_order_id = fsm_order.id
        FROM fsm_order
        WHERE fsm_order.repair_id IS NOT NULL
        AND repair_order.id = fsm_order.repair_id
        """,
    )
