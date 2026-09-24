-- ============================================================
-- Budidaya Krisan Pro — Database Schema (PostgreSQL / SQLite)
-- AI-Powered Chrysanthemum Cultivation Management Platform
-- ============================================================

-- Tabel master varietas krisan
CREATE TABLE IF NOT EXISTS varieties (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT DEFAULT 'spray',
    origin TEXT DEFAULT 'Jepang',
    cycle_days INTEGER DEFAULT 112,
    target_height_cm REAL DEFAULT 75,
    flowers_per_stem INTEGER DEFAULT 8,
    vase_life_days INTEGER DEFAULT 14,
    market_grade_a_price INTEGER DEFAULT 25000,
    description TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Tabel batch / siklus tanam
CREATE TABLE IF NOT EXISTS cultivation_batches (
    id TEXT PRIMARY KEY,
    batch_code TEXT UNIQUE NOT NULL,
    variety_id TEXT REFERENCES varieties(id),
    variety_name TEXT NOT NULL,
    planting_date TEXT NOT NULL,
    target_harvest_date TEXT NOT NULL,
    land_area_m2 REAL DEFAULT 600,
    plant_count INTEGER DEFAULT 28800,
    house_name TEXT DEFAULT 'House 1',
    beds_count INTEGER DEFAULT 12,
    bed_length_m REAL DEFAULT 50.0,
    row_count INTEGER DEFAULT 6,
    plant_spacing_cm REAL DEFAULT 12.5,
    status TEXT DEFAULT 'active' CHECK(status IN ('active','harvested','failed')),
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Tabel data pertumbuhan mingguan
CREATE TABLE IF NOT EXISTS growth_records (
    id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL REFERENCES cultivation_batches(id) ON DELETE CASCADE,
    batch_code TEXT NOT NULL,
    variety_name TEXT NOT NULL,
    week_number INTEGER NOT NULL,
    recording_date TEXT NOT NULL,
    plant_height_cm REAL,
    leaf_count INTEGER,
    stem_diameter_mm REAL,
    branch_count INTEGER,
    bud_count INTEGER DEFAULT 0,
    health_score REAL,
    ai_grade TEXT DEFAULT 'C',
    growth_deviation_pct REAL,
    anomaly_detected INTEGER DEFAULT 0,
    anomaly_type TEXT,
    temperature_c REAL,
    humidity_pct REAL,
    weather_condition TEXT DEFAULT 'cerah',
    notes TEXT,
    status TEXT DEFAULT 'recorded',
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(batch_id, week_number)
);

-- Tabel hasil panen
CREATE TABLE IF NOT EXISTS harvest_records (
    id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL REFERENCES cultivation_batches(id),
    batch_code TEXT NOT NULL,
    variety_name TEXT NOT NULL,
    harvest_date TEXT NOT NULL,
    total_stems INTEGER DEFAULT 0,
    grade_a_stems INTEGER DEFAULT 0,
    grade_b_stems INTEGER DEFAULT 0,
    grade_c_stems INTEGER DEFAULT 0,
    grade_a_price INTEGER DEFAULT 0,
    grade_b_price INTEGER DEFAULT 0,
    grade_c_price INTEGER DEFAULT 0,
    gross_revenue INTEGER DEFAULT 0,
    production_cost INTEGER DEFAULT 0,
    net_profit INTEGER DEFAULT 0,
    roi_pct REAL DEFAULT 0,
    bep_per_stem REAL DEFAULT 0,
    marketable_yield_pct REAL DEFAULT 0,
    loss_rate_pct REAL DEFAULT 0,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Tabel detail grading per grade per warna varietas (ikat-based)
CREATE TABLE IF NOT EXISTS harvest_detail_grades (
    id TEXT PRIMARY KEY,
    harvest_id TEXT NOT NULL REFERENCES harvest_records(id) ON DELETE CASCADE,
    batch_code TEXT NOT NULL,
    warna TEXT NOT NULL,
    grade_key TEXT NOT NULL,
    grade_name TEXT NOT NULL,
    tipe TEXT NOT NULL,
    stems_per_ikat INTEGER NOT NULL,
    jml_ikat INTEGER NOT NULL DEFAULT 0,
    total_batang INTEGER NOT NULL DEFAULT 0,
    harga_per_batang INTEGER NOT NULL DEFAULT 0,
    harga_per_ikat INTEGER NOT NULL DEFAULT 0,
    total_pendapatan INTEGER NOT NULL DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Tabel jurnal biaya harian operasional
CREATE TABLE IF NOT EXISTS cost_journal (
    id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL REFERENCES cultivation_batches(id) ON DELETE CASCADE,
    batch_code TEXT,
    tanggal TEXT NOT NULL,
    kategori TEXT NOT NULL,
    deskripsi TEXT,
    jumlah INTEGER NOT NULL DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Tabel konfigurasi webhook & notifikasi
CREATE TABLE IF NOT EXISTS webhook_config (
    id INTEGER PRIMARY KEY DEFAULT 1,
    webhook_url TEXT,
    is_enabled INTEGER DEFAULT 0,
    last_sent_at TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Index untuk performa
CREATE INDEX IF NOT EXISTS idx_growth_batch ON growth_records(batch_id);
CREATE INDEX IF NOT EXISTS idx_growth_week ON growth_records(week_number);
CREATE INDEX IF NOT EXISTS idx_growth_date ON growth_records(recording_date);
CREATE INDEX IF NOT EXISTS idx_batch_status ON cultivation_batches(status);
CREATE INDEX IF NOT EXISTS idx_harvest_batch ON harvest_records(batch_id);
CREATE INDEX IF NOT EXISTS idx_detail_grades_harvest ON harvest_detail_grades(harvest_id);
CREATE INDEX IF NOT EXISTS idx_cost_journal_batch ON cost_journal(batch_id);
