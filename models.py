import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "uangsadar.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            tipe        TEXT NOT NULL CHECK(tipe IN ('pemasukan','pengeluaran')),
            kategori    TEXT NOT NULL,
            jumlah      REAL NOT NULL,
            catatan     TEXT,
            tanggal     TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS target (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            nama              TEXT NOT NULL,
            jumlah_target     REAL NOT NULL,
            jumlah_terkumpul  REAL NOT NULL DEFAULT 0,
            deadline          TEXT,
            selesai           INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS chat_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            pesan_user  TEXT NOT NULL,
            balasan_bot TEXT NOT NULL,
            waktu       TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


# ── Transaksi ──────────────────────────────────────────────────────────────

def tambah_transaksi(tipe, kategori, jumlah, catatan, tanggal):
    conn = get_db()
    conn.execute(
        "INSERT INTO transaksi (tipe, kategori, jumlah, catatan, tanggal) VALUES (?,?,?,?,?)",
        (tipe, kategori, jumlah, catatan, tanggal),
    )
    conn.commit()
    conn.close()


def get_transaksi_semua():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM transaksi ORDER BY tanggal DESC, id DESC"
    ).fetchall()
    conn.close()
    return rows


def hapus_transaksi(tid):
    conn = get_db()
    conn.execute("DELETE FROM transaksi WHERE id = ?", (tid,))
    conn.commit()
    conn.close()


def get_ringkasan():
    conn = get_db()
    row = conn.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN tipe='pemasukan'   THEN jumlah ELSE 0 END), 0) AS total_masuk,
            COALESCE(SUM(CASE WHEN tipe='pengeluaran' THEN jumlah ELSE 0 END), 0) AS total_keluar
        FROM transaksi
    """).fetchone()
    conn.close()
    return dict(row)


# ── Target ─────────────────────────────────────────────────────────────────

def tambah_target(nama, jumlah_target, deadline):
    conn = get_db()
    conn.execute(
        "INSERT INTO target (nama, jumlah_target, deadline) VALUES (?,?,?)",
        (nama, jumlah_target, deadline),
    )
    conn.commit()
    conn.close()


def get_target_semua():
    conn = get_db()
    rows = conn.execute("SELECT * FROM target ORDER BY selesai, id DESC").fetchall()
    conn.close()
    return rows


def setor_target(tid, jumlah):
    conn = get_db()
    conn.execute("""
        UPDATE target
        SET jumlah_terkumpul = MIN(jumlah_target, jumlah_terkumpul + ?),
            selesai = CASE WHEN jumlah_terkumpul + ? >= jumlah_target THEN 1 ELSE 0 END
        WHERE id = ?
    """, (jumlah, jumlah, tid))
    conn.commit()
    conn.close()


def hapus_target(tid):
    conn = get_db()
    conn.execute("DELETE FROM target WHERE id = ?", (tid,))
    conn.commit()
    conn.close()


# ── Chat Log ───────────────────────────────────────────────────────────────

def simpan_chat(pesan_user, balasan_bot):
    conn = get_db()
    conn.execute(
        "INSERT INTO chat_log (pesan_user, balasan_bot, waktu) VALUES (?,?,?)",
        (pesan_user, balasan_bot, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()


def get_chat_log():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM chat_log ORDER BY id DESC LIMIT 30"
    ).fetchall()
    conn.close()
    return list(reversed(rows))
