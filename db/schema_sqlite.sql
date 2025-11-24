-- NucRadar v1 SQLite schema

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    ticker TEXT,
    country TEXT DEFAULT 'US',
    type TEXT,
    tech TEXT,
    website TEXT,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    source_type TEXT NOT NULL,
    base_url TEXT,
    details TEXT
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    source_id INTEGER,
    ts TEXT NOT NULL,
    ingested_at TEXT DEFAULT (datetime('now')),
    title TEXT NOT NULL,
    description TEXT,
    url TEXT,
    raw_payload TEXT,
    event_type TEXT,
    signal_level INTEGER,
    amount_usd REAL,
    currency TEXT DEFAULT 'USD',
    tags TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

CREATE INDEX IF NOT EXISTS idx_events_company_ts ON events (company_id, ts DESC);
CREATE INDEX IF NOT EXISTS idx_events_type_ts    ON events (event_type, ts DESC);
CREATE INDEX IF NOT EXISTS idx_events_signal_ts  ON events (signal_level, ts DESC);

CREATE TABLE IF NOT EXISTS fundraising_rounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    round TEXT,
    amount_usd REAL,
    currency TEXT DEFAULT 'USD',
    announced_date TEXT,
    lead_investors TEXT,
    notes TEXT,
    source_event_id INTEGER,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (source_event_id) REFERENCES events(id)
);
