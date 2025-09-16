import csv, pathlib, sqlite3, time
from datetime import datetime
LOG_DIR = pathlib.Path("logs")
LOG_DIR.mkdir(exist_ok=True)
CSV_PATH = LOG_DIR / "run.csv"
DB_PATH = LOG_DIR / "run.sqlite3"

def init_csv():
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "test_id","timestamp","model","attack_class","prompt",
                "expected","output","impact_label","reproducible",
                "http_status","attempts","notes"
            ])

def csv_append(row):
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)

def db_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs(
          test_id TEXT PRIMARY KEY,
          timestamp TEXT,
          model TEXT,
          attack_class TEXT,
          prompt TEXT,
          expected TEXT,
          output TEXT,
          impact_label TEXT,
          reproducible INTEGER,
          http_status INTEGER,
          attempts INTEGER,
          notes TEXT
        )
    """)
    conn.commit()
    return conn

def db_upsert(conn, row):
    conn.execute("""
    INSERT INTO logs(test_id,timestamp,model,attack_class,prompt,expected,output,impact_label,reproducible,http_status,attempts,notes)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
    ON CONFLICT(test_id) DO UPDATE SET
      timestamp=excluded.timestamp,
      model=excluded.model,
      attack_class=excluded.attack_class,
      prompt=excluded.prompt,
      expected=excluded.expected,
      output=excluded.output,
      impact_label=excluded.impact_label,
      reproducible=excluded.reproducible,
      http_status=excluded.http_status,
      attempts=excluded.attempts,
      notes=excluded.notes
    """, row)
    conn.commit()

def now_iso():
    return datetime.utcfromtimestamp(time.time()).isoformat() + "Z"
