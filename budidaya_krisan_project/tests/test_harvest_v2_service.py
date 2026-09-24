import pytest
from app.schemas.harvest_v2 import (
    HarvestRecordV2Create,
    WarnaGrading,
    GradeInput,
)
from app.services.harvest_v2_service import (
    compute_harvest_v2,
    save_cost_journal,
    get_cost_journal_summary,
)


def test_compute_harvest_v2_financials():
    """Verify ikat-based grading calculation and profit/ROI formulas."""
    sample_batch = {
        "batch_code": "KRISAN-DEMO-TEST",
        "variety_name": "Fiji White",
    }
    payload = HarvestRecordV2Create(
        batch_id="b_test",
        harvest_date="2026-10-25",
        house_name="House 1",
        biaya_operasional=50000000,
        biaya_penyusutan=10000000,
        harga_ekspektasi_per_btg=1000,
        varieties=[
            WarnaGrading(
                warna="Putih",
                bedengan=12,
                grades=[
                    GradeInput(
                        grade_key="g80",       # 80 stems/ikat, Normal
                        jml_ikat=300,          # 300 * 80 = 24,000 stems
                        harga_per_batang=1200, # 24,000 * 1,200 = 28,800,000
                    ),
                    GradeInput(
                        grade_key="g100",      # 100 stems/ikat, Normal
                        jml_ikat=300,          # 300 * 100 = 30,000 stems
                        harga_per_batang=1000, # 30,000 * 1,000 = 30,000,000
                    ),
                    GradeInput(
                        grade_key="r80",       # 80 stems/ikat, BS/Reject
                        jml_ikat=75,           # 75 * 80 = 6,000 stems
                        harga_per_batang=500,  # 6,000 * 500 = 3,000,000
                    ),
                ]
            )
        ]
    )

    summary, detail_rows = compute_harvest_v2(payload, sample_batch)

    assert summary["total_stems"] == 60000
    assert summary["grade_normal_stems"] == 54000
    assert summary["grade_bs_stems"] == 6000
    expected_revenue = 28800000 + 30000000 + 3000000  # 61,800,000
    assert summary["gross_revenue"] == expected_revenue
    assert summary["production_cost"] == 60000000
    assert summary["net_profit"] == expected_revenue - 60000000
    assert summary["roi_pct"] == round(((expected_revenue - 60000000) / 60000000) * 100, 2)
    assert summary["bep_per_stem"] == round(60000000 / 60000, 2)
    assert len(detail_rows) == 3


def test_cost_journal_entry_and_summary():
    """Verify operational cost journal insertion and aggregate summary."""
    batch_id = "b001"
    entry = save_cost_journal(
        batch_id=batch_id,
        batch_code="KRISAN-DEMO-001",
        tanggal="2026-08-30",
        kategori="Pupuk & Nutrisi",
        deskripsi="Pupuk kalium KNO3 putih fase generatif",
        jumlah=3200000,
    )
    assert entry["jumlah"] == 3200000
    assert entry["kategori"] == "Pupuk & Nutrisi"

    summary = get_cost_journal_summary(batch_id)
    assert "by_kategori" in summary
    assert summary["total_aktual"] >= 3200000
