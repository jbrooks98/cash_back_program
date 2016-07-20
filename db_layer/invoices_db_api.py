#!/usr/bin/env python
import sqlite3
import itertools
from decimal import Decimal
from conf import (
    DB_NAME, CASH_BACK_PERCENTAGE, ACCRUAL_INVOICE_PAYOUT
)

TABLE_NAME = 'invoices'


def create_invoice_table():
    """
    creates the invoice table
    Args:
        N/A

    Returns:
        N/A
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE {} (id INTEGER PRIMARY \
        KEY AUTOINCREMENT, invoice_amount DECIMAL NOT NULL, \
        customer_id INTEGER, accrual_amt DECIMAL, \
        accrual_paid_date NUMERIC, \
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id) \
        );".format(TABLE_NAME)
    )
    conn.commit()
    conn.close()


def delete_invoice_table():
    """
    deletes the invoice table
    Args:
        N/A

    Returns:
        N/A
    """

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE {};".format(TABLE_NAME))

    conn.commit()
    conn.close()


def create_invoice(customer_id, invoice_amount):
    """
    creates an invoice from the invoices table

    Args:
        customer_id: the id of customer the invoice is for
        invoice_amount: the dollar amount for the invoice

    Returns:
        total_changes
    """
    cash_back_percent = Decimal(CASH_BACK_PERCENTAGE) / Decimal(100)
    accrual_amt = (invoice_amount * cash_back_percent).quantize(
        Decimal('1.00')
    )

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO {table} (customer_id, invoice_amount, "
        "accrual_amt) VALUES ('{customer}', "
        "'{invoice_amount}', '{accrual_amt}');".format(
            table=TABLE_NAME,
            customer=customer_id,
            invoice_amount=invoice_amount,
            accrual_amt=accrual_amt)
    )

    conn.commit()
    total_changes = conn.total_changes
    conn.close()

    return total_changes


def delete_invoice(invoice_id):
    """
    deletes an invoice from the invoices table

    Args:
        invoice_id: the id of the invoice

    Returns:
        N/A
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM {0} WHERE id = {1};".format(
        TABLE_NAME,
        invoice_id)
    )
    conn.commit()
    conn.close()

    return


def update_invoice_accrual_paid_date(invoice_ids):
    """
    updates an invoice to indicate payment has been sent

    Args:
        invoice_ids: list of invoice ids

    Returns:
        N/A
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "UPDATE {0} SET accrual_paid_date = DateTime('now')"
        "WHERE id IN ({1});".format(TABLE_NAME, invoice_ids)
    )
    conn.commit()
    conn.close()

    return


def dict_gen(curs):
    """
    Generates a python dict from a sqlite result set

    Args:
        curs: cursor object

    Returns:
        generator object
    """
    field_names = [d[0].lower() for d in curs.description]

    while True:
        rows = curs.fetchmany()

        if not rows:
            return

        for row in rows:
            yield dict(itertools.izip(field_names, row))


def get_accrual_payouts():
    """
    Gets the total accrual amount owed to customers that are due payment

    Args:
        N/A

    Returns:
        list of dictionaries of the sql result set
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    sql = "SELECT SUM(accrual_amt) AS total_accrual_amt, \
        GROUP_CONCAT(id) AS invoice_ids, customer_id FROM \
        {0} WHERE accrual_paid_date IS null or accrual_paid_date = '' \
        GROUP BY customer_id HAVING count(*) > {1};".format(
            TABLE_NAME,
            ACCRUAL_INVOICE_PAYOUT)

    results = [r for r in dict_gen(c.execute(sql))]

    conn.close()

    return results






