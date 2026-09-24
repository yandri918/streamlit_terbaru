-- ============================================================
-- Budidaya Krisan Pro — PostgreSQL Seed Data
-- Data Master Varietas & Sampel Budidaya untuk Cloud Database
-- ============================================================

-- 1. Varietas Krisan Spray Jepang
INSERT INTO varieties (id, name, type, origin, cycle_days, target_height_cm, flowers_per_stem, vase_life_days, market_grade_a_price, description)
VALUES
    ('v001', 'Fiji White',    'spray', 'Jepang', 112, 75.0, 10, 14, 28000, 'Bunga putih bersih, tangkai kuat, cocok dataran tinggi 1000-1500 mdpl'),
    ('v002', 'Fiji Yellow',   'spray', 'Jepang', 112, 72.0, 10, 14, 26000, 'Bunga kuning cerah, populer ekspor, tahan cuaca'),
    ('v003', 'Reagent White', 'spray', 'Jepang', 105, 70.0, 12, 16, 30000, 'Mutu premium, bunga padat, vase life terpanjang'),
    ('v004', 'Reagent Pink',  'spray', 'Jepang', 105, 70.0, 12, 16, 30000, 'Warna pink lembut, sangat diminati pasar bunga segar'),
    ('v005', 'Princess White','spray', 'Jepang', 110, 73.0, 8, 14, 25000, 'Bunga pompon kecil rapi, cocok rangkaian'),
    ('v006', 'Gold Princess', 'spray', 'Jepang', 110, 73.0, 8, 14, 25000, 'Warna golden, tahan layu, disukai florist'),
    ('v007', 'Benson White',  'spray', 'Jepang', 108, 72.0, 9, 15, 27000, 'Ketahanan tinggi terhadap Fusarium, stabil'),
    ('v008', 'Benson Yellow', 'spray', 'Jepang', 108, 72.0, 9, 15, 27000, 'Varian kuning dari Benson series, produktif')
ON CONFLICT (id) DO NOTHING;

-- 2. Konfigurasi Webhook Default
INSERT INTO webhook_config (id, webhook_url, is_enabled)
VALUES (1, '', 0)
ON CONFLICT (id) DO NOTHING;

-- 3. Data Sampel Batch Budidaya
INSERT INTO cultivation_batches (id, batch_code, variety_id, variety_name, planting_date, target_harvest_date, land_area_m2, plant_count, house_name, beds_count, bed_length_m, row_count, plant_spacing_cm, status, notes)
VALUES
    ('b001', 'KRISAN-DEMO-001', 'v001', 'Fiji White', '2026-07-01', '2026-10-21', 600.0, 28800, 'House 1', 12, 50.0, 6, 12.5, 'active', 'Siklus utama House 1 - Fiji White spray ekspor'),
    ('b002', 'KRISAN-DEMO-002', 'v002', 'Fiji Yellow', '2026-08-01', '2026-11-21', 600.0, 28800, 'House 2', 12, 50.0, 6, 12.5, 'active', 'Siklus House 2 - Fiji Yellow pasar domestik & florist'),
    ('b003', 'KRISAN-DEMO-003', 'v004', 'Reagent Pink', '2026-03-01', '2026-06-21', 600.0, 28800, 'House 3', 12, 50.0, 6, 12.5, 'harvested', 'Siklus panen sukses House 3 - Reagent Pink')
ON CONFLICT (id) DO UPDATE SET
    batch_code = EXCLUDED.batch_code,
    variety_name = EXCLUDED.variety_name,
    status = EXCLUDED.status;

-- 4. Data Sampel Pertumbuhan Mingguan (Batch 1: House 1 - Fiji White)
INSERT INTO growth_records (id, batch_id, batch_code, variety_name, week_number, recording_date, plant_height_cm, leaf_count, stem_diameter_mm, branch_count, bud_count, health_score, ai_grade, growth_deviation_pct, anomaly_detected, anomaly_type, temperature_c, humidity_pct, weather_condition, notes, status)
VALUES
    ('gr001', 'b001', 'KRISAN-DEMO-001', 'Fiji White', 1, '2026-07-08', 12.5, 6, 4.2, 0, 0, 92.5, 'A', 4.17, 0, NULL, 18.5, 78.0, 'cerah', 'Stek berakar sempurna, adaptasi baik', 'recorded'),
    ('gr002', 'b001', 'KRISAN-DEMO-001', 'Fiji White', 2, '2026-07-15', 16.8, 8, 4.8, 0, 0, 94.0, 'A', 5.00, 0, NULL, 19.0, 76.0, 'cerah', 'Pertumbuhan daun baru serempak', 'recorded'),
    ('gr003', 'b001', 'KRISAN-DEMO-001', 'Fiji White', 3, '2026-07-22', 21.5, 10, 5.2, 0, 0, 93.5, 'A', 2.38, 0, NULL, 18.2, 80.0, 'berawan', 'Fertigasi vegetatif awal berjalan optimal', 'recorded'),
    ('gr004', 'b001', 'KRISAN-DEMO-001', 'Fiji White', 4, '2026-07-29', 27.2, 12, 5.6, 0, 0, 95.0, 'A', 4.62, 0, NULL, 18.8, 77.0, 'cerah', 'Batang kokoh, daun hijau tua mengkilap', 'recorded'),
    ('gr005', 'b001', 'KRISAN-DEMO-001', 'Fiji White', 5, '2026-08-05', 33.8, 14, 6.0, 0, 0, 94.5, 'A', 2.42, 0, NULL, 19.2, 75.0, 'cerah', 'Persiapan pinching minggu ke-7', 'recorded'),
    ('gr006', 'b001', 'KRISAN-DEMO-001', 'Fiji White', 6, '2026-08-12', 41.5, 16, 6.4, 0, 0, 93.0, 'A', 1.22, 0, NULL, 18.0, 82.0, 'hujan ringan', 'Tinggi ideal sesuai standar Balithi', 'recorded'),
    ('gr007', 'b001', 'KRISAN-DEMO-001', 'Fiji White', 7, '2026-08-19', 49.5, 18, 6.8, 4, 0, 96.0, 'A', 3.12, 0, NULL, 18.5, 78.0, 'cerah', 'Pinching pucuk dilakukan, 4 cabang produktif muncul', 'recorded'),
    ('gr008', 'b001', 'KRISAN-DEMO-001', 'Fiji White', 8, '2026-08-26', 58.2, 20, 7.2, 4, 0, 95.5, 'A', 3.93, 0, NULL, 19.1, 74.0, 'cerah', 'Cabang produktif memanjang seragam', 'recorded')
ON CONFLICT (id) DO NOTHING;

-- 5. Data Sampel Pertumbuhan Mingguan (Batch 2: House 2 - Fiji Yellow)
INSERT INTO growth_records (id, batch_id, batch_code, variety_name, week_number, recording_date, plant_height_cm, leaf_count, stem_diameter_mm, branch_count, bud_count, health_score, ai_grade, growth_deviation_pct, anomaly_detected, anomaly_type, temperature_c, humidity_pct, weather_condition, notes, status)
VALUES
    ('gr009', 'b002', 'KRISAN-DEMO-002', 'Fiji Yellow', 1, '2026-08-08', 11.8, 6, 4.0, 0, 0, 89.0, 'A', -1.67, 0, NULL, 18.6, 79.0, 'cerah', 'Penanaman bibit House 2 sukses', 'recorded'),
    ('gr010', 'b002', 'KRISAN-DEMO-002', 'Fiji Yellow', 2, '2026-08-15', 15.6, 8, 4.5, 0, 0, 90.5, 'A', -2.50, 0, NULL, 18.4, 80.0, 'cerah', 'Pertumbuhan akar kuat', 'recorded'),
    ('gr011', 'b002', 'KRISAN-DEMO-002', 'Fiji Yellow', 3, '2026-08-22', 20.8, 10, 5.0, 0, 0, 91.0, 'A', -0.95, 0, NULL, 18.9, 76.0, 'cerah', 'Perkembangan vegetatif stabil', 'recorded'),
    ('gr012', 'b002', 'KRISAN-DEMO-002', 'Fiji Yellow', 4, '2026-08-29', 26.5, 12, 5.4, 0, 0, 92.5, 'A', 1.92, 0, NULL, 19.0, 75.0, 'cerah', 'Kondisi tanaman sehat dan tegak', 'recorded')
ON CONFLICT (id) DO NOTHING;

-- 6. Data Sampel Hasil Panen (Batch 3: House 3 - Reagent Pink)
INSERT INTO harvest_records (id, batch_id, batch_code, variety_name, harvest_date, total_stems, grade_a_stems, grade_b_stems, grade_c_stems, grade_a_price, grade_b_price, grade_c_price, gross_revenue, production_cost, net_profit, roi_pct, bep_per_stem, marketable_yield_pct, loss_rate_pct, notes)
VALUES
    ('h001', 'b003', 'KRISAN-DEMO-003', 'Reagent Pink', '2026-06-25', 85680, 59976, 21420, 4284, 30000, 22000, 12000, 232188000, 138000000, 94188000, 68.25, 1610.64, 95.0, 5.0, 'Panen raya House 3 Reagent Pink dengan kualitas ekspor Grade A mencapai 70%')
ON CONFLICT (id) DO NOTHING;

-- 7. Data Detail Grading Ikat-Based
INSERT INTO harvest_detail_grades (id, harvest_id, batch_code, warna, grade_key, grade_name, tipe, stems_per_ikat, jml_ikat, total_batang, harga_per_batang, harga_per_ikat, total_pendapatan)
VALUES
    ('hd001', 'h001', 'KRISAN-DEMO-003', 'Pink', 'normal_aa', 'Grade AA (Premium)', 'Normal', 10, 3200, 32000, 3200, 32000, 102400000),
    ('hd002', 'h001', 'KRISAN-DEMO-003', 'Pink', 'normal_a', 'Grade A (Standar)', 'Normal', 10, 2797, 27976, 2800, 28000, 78332800),
    ('hd003', 'h001', 'KRISAN-DEMO-003', 'Pink', 'normal_b', 'Grade B (Medium)', 'Normal', 10, 2142, 21420, 2200, 22000, 47124000),
    ('hd004', 'h001', 'KRISAN-DEMO-003', 'Pink', 'bs_pendek', 'BS Pendek', 'BS', 10, 428, 4284, 1000, 10000, 4284000)
ON CONFLICT (id) DO NOTHING;

-- 8. Data Jurnal Biaya Operasional
INSERT INTO cost_journal (id, batch_id, batch_code, tanggal, kategori, deskripsi, jumlah)
VALUES
    ('cj001', 'b001', 'KRISAN-DEMO-001', '2026-06-25', 'Bibit & Stek', 'Pengadaan 30.000 stek berakar Fiji White Grade A', 15000000),
    ('cj002', 'b001', 'KRISAN-DEMO-001', '2026-06-28', 'Media & Olah Tanah', 'Arang sekam, pupuk kandang matang, kapur dolomit', 6500000),
    ('cj003', 'b001', 'KRISAN-DEMO-001', '2026-07-05', 'Pupuk & Nutrisi', 'Pupuk NPK 25:7:7 vegetatif + mikro fertigasi', 4800000),
    ('cj004', 'b001', 'KRISAN-DEMO-001', '2026-07-15', 'Listrik & Lampu', 'Penerangan malam (long day lighting) siklus vegetatif', 2400000),
    ('cj005', 'b001', 'KRISAN-DEMO-001', '2026-08-19', 'Tenaga Kerja', 'Pinching tunas pucuk & sanitasi gulma 12 bedengan', 1800000)
ON CONFLICT (id) DO NOTHING;
