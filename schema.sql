-- schema.sql

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS transaction_types (
  id   INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL        -- e.g. 'incoming', 'payment', 'transfer', 'deposit', 'airtime', 'cash_power', 'withdrawal', 'otp'
);

CREATE TABLE IF NOT EXISTS transactions (
  id                  INTEGER PRIMARY KEY AUTOINCREMENT,
  sms_id              TEXT    UNIQUE NOT NULL,     -- e.g. XML attribute <sms protocol+address+date>
  raw_body            TEXT    NOT NULL,
  tx_type_id          INTEGER NOT NULL REFERENCES transaction_types(id),
  amount              INTEGER NOT NULL,            -- in RWF
  currency            TEXT    NOT NULL,            -- 'RWF'
  fee                 INTEGER DEFAULT 0,
  balance_after       INTEGER,                     -- new balance
  tx_timestamp        DATETIME NOT NULL,
  from_party          TEXT,                        -- could be NULL (e.g. deposits)
  to_party            TEXT,                        -- could be NULL (e.g. incoming)
  momo_tx_id          TEXT,                        -- provider’s transaction ID
  agent_id            TEXT,                        -- for agent withdrawals/deposits
  extra_info          TEXT                         -- JSON for any other fields
);
