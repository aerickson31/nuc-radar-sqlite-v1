import os
import json
import yaml
import sqlite3
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "etl", "config.yaml")
DB_PATH = os.path.join(BASE_DIR, "nuc_radar.sqlite")

with open(CONFIG_PATH) as f:
    cfg = yaml.safe_load(f)

def get_conn():
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def get_or_create_company(conn, name, slug):
    cur = conn.cursor()
    cur.execute("SELECT id FROM companies WHERE slug = ?", (slug,))
    row = cur.fetchone()
    if row:
        return row["id"]
    cur.execute(
        "INSERT INTO companies (name, slug) VALUES (?, ?)",
        (name, slug),
    )
    conn.commit()
    return cur.lastrowid

def get_or_create_source(conn, name):
    cur = conn.cursor()
    cur.execute("SELECT id FROM sources WHERE name = ?", (name,))
    row = cur.fetchone()
    if row:
        return row["id"]
    cur.execute(
        "INSERT INTO sources (name, source_type) VALUES (?, ?)",
        (name, "news_api"),
    )
    conn.commit()
    return cur.lastrowid

def classify_article(article):
    title = (article.get("headline") or article.get("title") or "").lower()
    desc = (article.get("summary") or article.get("description") or "").lower()
    text = title + " " + desc

    event_type = "marketing"
    signal = 1
    tags = []

    if any(x in text for x in ["series a", "series b", "series c", "funding round", "raised"]):
        event_type = "fundraise"
        signal = 4
        tags.append("fundraise")

    if "department of energy" in text or "doe" in text or "reactor pilot program" in text or "gain voucher" in text:
        event_type = "gov_program"
        signal = max(signal, 3)
        tags.append("DOE")

    if "nrc" in text or "license" in text or "part 50" in text or "part 52" in text:
        event_type = "regulatory"
        signal = 5
        tags.append("NRC")

    if "cold criticality" in text or "zero power" in text or "subcritical" in text:
        event_type = "hardware"
        signal = max(signal, 2)
        tags.append("experiment")

    return event_type, signal, tags

def upsert_event(conn, company_id, source_id, article):
    cur = conn.cursor()
    ts_val = article.get("datetime") or article.get("published_at") or datetime.utcnow().isoformat()
    if isinstance(ts_val, (int, float)):
        ts_str = datetime.utcfromtimestamp(ts_val).isoformat()
    else:
        ts_str = str(ts_val)

    title = (article.get("headline") or article.get("title") or "").strip()
    desc  = (article.get("summary")  or article.get("description") or "").strip()
    url   = (article.get("url") or "").strip()
    raw   = json.dumps(article)

    event_type, signal_level, tags = classify_article(article)
    tags_str = ",".join(tags) if tags else None

    cur.execute(
        "SELECT id FROM events WHERE company_id = ? AND ts = ? AND title = ?",
        (company_id, ts_str, title),
    )
    if cur.fetchone():
        return

    cur.execute(
        """INSERT INTO events
             (company_id, source_id, ts, title, description, url,
              raw_payload, event_type, signal_level, tags)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            company_id,
            source_id,
            ts_str,
            title,
            desc,
            url,
            raw,
            event_type,
            signal_level,
            tags_str,
        ),
    )
    conn.commit()

def fetch_articles_for_company(name):
    # TODO: replace with a real news API call later.
    now = datetime.utcnow().isoformat()
    return [{
        "headline": f"Test milestone for {name}",
        "summary": "Dummy article to test SQLite wiring",
        "url": "https://example.com/test",
        "datetime": now,
    }]

def main():
    conn = get_conn()
    src_id = get_or_create_source(conn, "DummyNews")
    since = datetime.utcnow() - timedelta(days=1)

    for c in cfg["companies"]:
        company_id = get_or_create_company(conn, c["name"], c["slug"])
        articles = fetch_articles_for_company(c["name"])
        for a in articles:
            upsert_event(conn, company_id, src_id, a)

    conn.close()

if __name__ == "__main__":
    main()
