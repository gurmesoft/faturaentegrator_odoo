"""fe.integration.temp -> fe.invoice.integration geçişinde sihirbaz FK'larını temizle."""


def migrate(cr, version):
    for table in ('fe_send_invoice_wizard', 'fe_send_order_wizard'):
        cr.execute(
            """
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = current_schema() AND table_name = %s
            """,
            (table,),
        )
        if not cr.fetchone():
            continue
        cr.execute(
            f"""
            UPDATE {table}
            SET integration_choice_id = NULL
            WHERE integration_choice_id IS NOT NULL
            """
        )
