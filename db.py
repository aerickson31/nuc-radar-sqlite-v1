import os
import sqlite3
import streamlit as st

DB_PATH = os.path.join(os.path.dirname(__file__), "nuc_radar.sqlite")

@st.cache_resource
def get_conn():
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def fetchall(query, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params or [])
    return cur.fetchall()

def fetchone(query, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params or [])
    return cur.fetchone()

def execute(query, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params or [])
    conn.commit()
    return cur.lastrowid
