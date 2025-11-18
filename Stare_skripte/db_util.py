# db_util.py
import os, sqlite3
from contextlib import contextmanager

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Absolutna pot do VUS.db v korenu projekta (symlink na var\data\VUS.db je OK)
DB_PATH = os.path.join(BASE_DIR, "VUS.db")

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
