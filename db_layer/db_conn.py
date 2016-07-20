#!/usr/bin/env python
import sqlite3


def connect_to_db(db_name):
    """
    creates a connection to the database
    Args:
        db_name:  Name of database

    Returns:
        database connection
    """
    return sqlite3.connect(db_name)
