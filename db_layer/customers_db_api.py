#!/usr/bin/env python
from accrual_conf import DB_NAME
from db_conn import connect_to_db


def create_customer_table():
    """
    creates the customer table
    Args:
        N/A

    Returns:
        N/A
    """
    conn = connect_to_db(DB_NAME)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE customers (id INTEGER PRIMARY
        KEY AUTOINCREMENT, name VARCHAR NOT NULL, CONSTRAINT name_unique
        UNIQUE (name))"""
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
    conn = connect_to_db(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE customers")

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
    conn = connect_to_db(DB_NAME)
    c = conn.cursor()

    c.execute(
        "INSERT OR IGNORE INTO customers (name) VALUES (?)", ([name])
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
    conn = connect_to_db(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT id, name FROM customers")

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
    conn = connect_to_db(DB_NAME)
    c = conn.cursor()

    c.execute(
        "SELECT name FROM customers WHERE id = ?", ([customer_id])
    )
    customer_name = c.fetchone()[0]
    conn.close()

    return customer_name



