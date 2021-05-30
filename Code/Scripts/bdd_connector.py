#!/usr/bin/python3

import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="jbalsells",
        password="",
        host="127.0.0.1",
        port=3306,
        database="unir_ingmate"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()