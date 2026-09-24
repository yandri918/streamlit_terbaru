"""
Harvest V2 Service — Ikat-Based Grading Calculator
Logika kalkulasi sesuai sistem asli Streamlit (Pasca Panen)
"""
from typing import Dict, List, Optional
from app.schemas.harvest_v2 import GRADE_CATALOG, NORMAL_GRADES, BS_GRADES, HarvestRecordV2Create
from app.services.db import get_db, new_id, rows_to_list


def compute_harvest_v2(payload: HarvestRecordV2Create, batch: Dict) -> Dict:
    """
    Hitung semua metrik finansial dari input ikat-based grading.
    Returns: summary dict + detail_rows list
    """
    detail_rows = []
    grand_total_batang = 0
    grand_total_pendapatan = 0
    grand_total_normal_btg = 0
    grand_total_bs_btg = 0

    per_warna_summary = {}

    for warna_item in payload.varieties:
        warna = warna_item.warna
        warna_batang = 0
        warna_normal_btg = 0
        warna_bs_btg = 0
        warna_pendapatan = 0

        for grade_input in warna_item.grades:
            key = grade_input.grade_key
            if key not in GRADE_CATALOG:
                continue
            if grade_input.jml_ikat <= 0:
                continue

            cat = GRADE_CATALOG[key]
            stems_per_ikat = cat["stems_per_ikat"]
            tipe = cat["tipe"]
            total_batang = grade_input.jml_ikat * stems_per_ikat
            harga_per_ikat = grade_input.harga_per_batang * stems_per_ikat
            total_pendapatan = total_batang * grade_input.harga_per_batang

            detail_rows.append({
                "warna": warna,
                "grade_key": key,
                "grade_name": cat["name"],
                "tipe": tipe,
                "stems_per_ikat": stems_per_ikat,
                "jml_ikat": grade_input.jml_ikat,
                "total_batang": total_batang,
                "harga_per_batang": grade_input.harga_per_batang,
                "harga_per_ikat": harga_per_ikat,
                "total_pendapatan": total_pendapatan,
            })

            warna_batang += total_batang
            warna_pendapatan += total_pendapatan
            if tipe == "Normal":
                warna_normal_btg += total_batang
            else:
                warna_bs_btg += total_batang

        per_warna_summary[warna] = {
            "warna": warna,
            "bedengan": warna_item.bedengan,
            "total_batang": warna_batang,
            "normal_batang": warna_normal_btg,
            "bs_batang": warna_bs_btg,
            "total_pendapatan": warna_pendapatan,
        }
        grand_total_batang += warna_batang
        grand_total_pendapatan += warna_pendapatan
        grand_total_normal_btg += warna_normal_btg
        grand_total_bs_btg += warna_bs_btg

    # Finansial
    total_biaya = payload.biaya_operasional + payload.biaya_penyusutan
    net_profit = grand_total_pendapatan - total_biaya
    roi = round((net_profit / max(1, total_biaya)) * 100, 2)
    bep_per_stem = round(total_biaya / max(1, grand_total_batang), 2)
    grade_a_pct = round(grand_total_normal_btg / max(1, grand_total_batang) * 100, 1)
    bs_pct = round(grand_total_bs_btg / max(1, grand_total_batang) * 100, 1)

    # Variance vs ekspektasi
    actual_price_per_stem = round(grand_total_pendapatan / max(1, grand_total_batang), 2)
    price_variance = round(actual_price_per_stem - payload.harga_ekspektasi_per_btg, 2)
    price_variance_pct = round((price_variance / max(1, payload.harga_ekspektasi_per_btg)) * 100, 2)
    expected_revenue = grand_total_batang * payload.harga_ekspektasi_per_btg
    profit_variance = grand_total_pendapatan - expected_revenue

    summary = {
        "batch_id": payload.batch_id,
        "batch_code": batch["batch_code"],
        "variety_name": batch["variety_name"],
        "house_name": payload.house_name,
        "harvest_date": payload.harvest_date,
        "total_stems": grand_total_batang,
        "grade_normal_stems": grand_total_normal_btg,
        "grade_bs_stems": grand_total_bs_btg,
        "gross_revenue": grand_total_pendapatan,
        "production_cost": total_biaya,
        "net_profit": net_profit,
        "roi_pct": roi,
        "bep_per_stem": bep_per_stem,
        "marketable_yield_pct": grade_a_pct,
        "loss_rate_pct": bs_pct,
        "grade_a_pct": grade_a_pct,
        "actual_price_per_stem": actual_price_per_stem,
        "harga_ekspektasi_per_btg": payload.harga_ekspektasi_per_btg,
        "price_variance": price_variance,
        "price_variance_pct": price_variance_pct,
        "profit_variance": profit_variance,
        "per_warna": per_warna_summary,
        "notes": payload.notes,
    }
    return summary, detail_rows


def save_harvest_v2(summary: Dict, detail_rows: List[Dict], harvest_id: str) -> bool:
    """Save harvest detail grades to DB."""
    try:
        with get_db() as conn:
            for row in detail_rows:
                conn.execute(
                    """INSERT INTO harvest_detail_grades
                       (id, harvest_id, batch_code, warna, grade_key, grade_name, tipe,
                        stems_per_ikat, jml_ikat, total_batang, harga_per_batang,
                        harga_per_ikat, total_pendapatan)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    [new_id(), harvest_id, summary["batch_code"],
                     row["warna"], row["grade_key"], row["grade_name"], row["tipe"],
                     row["stems_per_ikat"], row["jml_ikat"], row["total_batang"],
                     row["harga_per_batang"], row["harga_per_ikat"], row["total_pendapatan"]]
                )
        return True
    except Exception as e:
        raise e


def get_harvest_detail_grades(harvest_id: str) -> List[Dict]:
    with get_db() as conn:
        return rows_to_list(conn.execute(
            "SELECT * FROM harvest_detail_grades WHERE harvest_id=? ORDER BY warna, tipe, grade_key",
            [harvest_id]
        ).fetchall())


def save_cost_journal(batch_id: str, batch_code: str, tanggal: str,
                      kategori: str, deskripsi: str, jumlah: int) -> Dict:
    jid = new_id()
    from datetime import datetime
    with get_db() as conn:
        conn.execute(
            "INSERT INTO cost_journal (id, batch_id, batch_code, tanggal, kategori, deskripsi, jumlah) VALUES (?,?,?,?,?,?,?)",
            [jid, batch_id, batch_code, tanggal, kategori, deskripsi, jumlah]
        )
        row = conn.execute("SELECT * FROM cost_journal WHERE id=?", [jid]).fetchone()
        return dict(row)


def get_cost_journal(batch_id: Optional[str] = None) -> List[Dict]:
    with get_db() as conn:
        if batch_id:
            rows = conn.execute(
                "SELECT * FROM cost_journal WHERE batch_id=? ORDER BY tanggal DESC",
                [batch_id]
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM cost_journal ORDER BY tanggal DESC LIMIT 200"
            ).fetchall()
        return rows_to_list(rows)


def get_cost_journal_summary(batch_id: str) -> Dict:
    """Ringkasan jurnal biaya per kategori untuk satu batch."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT kategori, SUM(jumlah) as total FROM cost_journal WHERE batch_id=? GROUP BY kategori",
            [batch_id]
        ).fetchall()
        total_all = conn.execute(
            "SELECT SUM(jumlah) as total FROM cost_journal WHERE batch_id=?", [batch_id]
        ).fetchone()

    by_cat = {r["kategori"]: int(r["total"]) for r in rows}
    return {
        "by_kategori": by_cat,
        "total_aktual": int(total_all["total"] or 0),
    }
