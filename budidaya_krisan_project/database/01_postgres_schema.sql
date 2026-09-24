-- ============================================================
-- Budidaya Krisan Pro — PostgreSQL Database Schema
-- Production Cloud Database (Railway / Supabase / Neon)
-- ============================================================

-- 1. Tabel Master Varietas Krisan
CREATE TABLE IF NOT EXISTS varieties (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    type VARCHAR(64) DEFAULT 'spray',
    origin VARCHAR(64) DEFAULT 'Jepang',
    cycle_days INTEGER DEFAULT 112,
    target_height_cm NUMERIC(6, 2) DEFAULT 75.0,
    flowers_per_stem INTEGER DEFAULT 8,
    vase_life_days INTEGER DEFAULT 14,
    market_grade_a_price INTEGER DEFAULT 25000,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabel Batch / Siklus Tanam
CREATE TABLE IF NOT EXISTS cultivation_batches (
    id VARCHAR(64) PRIMARY KEY,
    batch_code VARCHAR(64) UNIQUE NOT NULL,
    variety_id VARCHAR(64) REFERENCES varieties(id) ON DELETE SET NULL,
    variety_name VARCHAR(128) NOT NULL,
    planting_date DATE NOT NULL,
    target_harvest_date DATE NOT NULL,
    land_area_m2 NUMERIC(10, 2) DEFAULT 600.0,
    plant_count INTEGER DEFAULT 28800,
    house_name VARCHAR(64) DEFAULT 'House 1',
    beds_count INTEGER DEFAULT 12,
    bed_length_m NUMERIC(8, 2) DEFAULT 50.0,
    row_count INTEGER DEFAULT 6,
    plant_spacing_cm NUMERIC(6, 2) DEFAULT 12.5,
    status VARCHAR(32) DEFAULT 'active' CHECK(status IN ('active', 'harvested', 'failed')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabel Data Pertumbuhan Mingguan
CREATE TABLE IF NOT EXISTS growth_records (
    id VARCHAR(64) PRIMARY KEY,
    batch_id VARCHAR(64) NOT NULL REFERENCES cultivation_batches(id) ON DELETE CASCADE,
    batch_code VARCHAR(64) NOT NULL,
    variety_name VARCHAR(128) NOT NULL,
    week_number INTEGER NOT NULL,
    recording_date DATE NOT NULL,
    plant_height_cm NUMERIC(6, 2),
    leaf_count INTEGER,
    stem_diameter_mm NUMERIC(6, 2),
    branch_count INTEGER,
    bud_count INTEGER DEFAULT 0,
    health_score NUMERIC(5, 2),
    ai_grade VARCHAR(8) DEFAULT 'C',
    growth_deviation_pct NUMERIC(6, 2),
    anomaly_detected INTEGER DEFAULT 0,
    anomaly_type VARCHAR(128),
    temperature_c NUMERIC(5, 2),
    humidity_pct NUMERIC(5, 2),
    weather_condition VARCHAR(64) DEFAULT 'cerah',
    notes TEXT,
    status VARCHAR(32) DEFAULT 'recorded',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_growth_batch_week UNIQUE(batch_id, week_number)
);

-- 4. Tabel Hasil Panen
CREATE TABLE IF NOT EXISTS harvest_records (
    id VARCHAR(64) PRIMARY KEY,
    batch_id VARCHAR(64) NOT NULL REFERENCES cultivation_batches(id) ON DELETE CASCADE,
    batch_code VARCHAR(64) NOT NULL,
    variety_name VARCHAR(128) NOT NULL,
    harvest_date DATE NOT NULL,
    total_stems INTEGER DEFAULT 0,
    grade_a_stems INTEGER DEFAULT 0,
    grade_b_stems INTEGER DEFAULT 0,
    grade_c_stems INTEGER DEFAULT 0,
    grade_a_price INTEGER DEFAULT 0,
    grade_b_price INTEGER DEFAULT 0,
    grade_c_price INTEGER DEFAULT 0,
    gross_revenue BIGINT DEFAULT 0,
    production_cost BIGINT DEFAULT 0,
    net_profit BIGINT DEFAULT 0,
    roi_pct NUMERIC(6, 2) DEFAULT 0,
    bep_per_stem NUMERIC(10, 2) DEFAULT 0,
    marketable_yield_pct NUMERIC(5, 2) DEFAULT 0,
    loss_rate_pct NUMERIC(5, 2) DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabel Detail Grading Per Grade Per Warna (Ikat-Based)
CREATE TABLE IF NOT EXISTS harvest_detail_grades (
    id VARCHAR(64) PRIMARY KEY,
    harvest_id VARCHAR(64) NOT NULL REFERENCES harvest_records(id) ON DELETE CASCADE,
    batch_code VARCHAR(64) NOT NULL,
    warna VARCHAR(64) NOT NULL,
    grade_key VARCHAR(64) NOT NULL,
    grade_name VARCHAR(128) NOT NULL,
    tipe VARCHAR(32) NOT NULL,
    stems_per_ikat INTEGER NOT NULL,
    jml_ikat INTEGER NOT NULL DEFAULT 0,
    total_batang INTEGER NOT NULL DEFAULT 0,
    harga_per_batang INTEGER NOT NULL DEFAULT 0,
    harga_per_ikat INTEGER NOT NULL DEFAULT 0,
    total_pendapatan BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Tabel Jurnal Biaya Operasional Harian
CREATE TABLE IF NOT EXISTS cost_journal (
    id VARCHAR(64) PRIMARY KEY,
    batch_id VARCHAR(64) NOT NULL REFERENCES cultivation_batches(id) ON DELETE CASCADE,
    batch_code VARCHAR(64),
    tanggal DATE NOT NULL,
    kategori VARCHAR(64) NOT NULL,
    deskripsi TEXT,
    jumlah BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Tabel Konfigurasi Webhook
CREATE TABLE IF NOT EXISTS webhook_config (
    id INTEGER PRIMARY KEY DEFAULT 1,
    webhook_url TEXT,
    is_enabled INTEGER DEFAULT 0,
    last_sent_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indeks Performa
CREATE INDEX IF NOT EXISTS idx_pg_growth_batch ON growth_records(batch_id);
CREATE INDEX IF NOT EXISTS idx_pg_growth_week ON growth_records(week_number);
CREATE INDEX IF NOT EXISTS idx_pg_growth_date ON growth_records(recording_date);
CREATE INDEX IF NOT EXISTS idx_pg_batch_status ON cultivation_batches(status);
CREATE INDEX IF NOT EXISTS idx_pg_harvest_batch ON harvest_records(batch_id);
CREATE INDEX IF NOT EXISTS idx_pg_detail_grades_harvest ON harvest_detail_grades(harvest_id);
CREATE INDEX IF NOT EXISTS idx_pg_cost_journal_batch ON cost_journal(batch_id);
