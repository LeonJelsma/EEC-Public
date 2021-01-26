from os.path import join as join
import os

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = join(SRC_DIR, "db")
DB_FILE = join(DB_DIR, "database.db")
