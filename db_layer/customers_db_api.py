#!/usr/bin/env python
import sqlite3
from accrual_conf import DB_NAME


TABLE_NAME = 'customers'


def create_customer_table():
    """
    creates the customer table
    Args:
        N/A

    Returns:
        N/A
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE {} (id INTEGER PRIMARY \
        KEY AUTOINCREMENT, name VARCHAR NOT NULL, CONSTRAINT name_unique \
        UNIQUE (name));".format(TABLE_NAME)
    )
    conn.commit()
    conn.close()

    return


def delete_customer_table():
    """
    deletes the customer table
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

    return


def create_customer(name):

    """
    creates a customer in the customer table
    Args:
        name: name of the customer (must be unique)

    Returns:
        N/A
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("INSERT OR IGNORE INTO {0} (name) VALUES ('{1}')".format(
        TABLE_NAME,
        name)
    )

    conn.commit()
    conn.close()

    return


def get_all_customers():
    """
    gets all customers in the customer table
    Args:
        N/A

    Returns:
        list of tuples of customer ids and names
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT id, name FROM {};".format(TABLE_NAME))

    customer_names = c.fetchall()
    conn.close()

    return customer_names


def get_customer_name(customer_id):
    """
    gets the name of a customer
    Args:
        customer_id

    Returns:
        customer name
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT name FROM {0} WHERE id = {1};".format(
        TABLE_NAME,
        customer_id)
    )

    customer_name = c.fetchone()[0]
    conn.close()

    return customer_name



