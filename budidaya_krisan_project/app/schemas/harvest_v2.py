"""
Harvest V2 Schemas — Ikat-Based Grading per Warna Varietas
Sesuai dengan sistem asli Streamlit (7_Pasca_Panen.py)
"""
from pydantic import BaseModel, Field
from typing import List, Optional


# ============================================================
# Definisi master 9 grade krisan spray (sesuai Streamlit asli)
# ============================================================
GRADE_CATALOG = {
    # Grade Normal — panjang tangkai 90 cm
    "g60":  {"name": "Grade 60",  "tipe": "Normal",    "stems_per_ikat": 60,  "default_price": 1000},
    "g80":  {"name": "Grade 80",  "tipe": "Normal",    "stems_per_ikat": 80,  "default_price": 1000},
    "g100": {"name": "Grade 100", "tipe": "Normal",    "stems_per_ikat": 100, "default_price": 1000},
    "g120": {"name": "Grade 120", "tipe": "Normal",    "stems_per_ikat": 120, "default_price": 1000},
    "g160": {"name": "Grade 160", "tipe": "Normal",    "stems_per_ikat": 160, "default_price": 1000},
    # Grade BS/Reject — panjang tangkai 70-80 cm
    "r80":  {"name": "R-80",      "tipe": "BS/Reject", "stems_per_ikat": 80,  "default_price": 500},
    "r100": {"name": "R-100",     "tipe": "BS/Reject", "stems_per_ikat": 100, "default_price": 500},
    "r160": {"name": "R-160",     "tipe": "BS/Reject", "stems_per_ikat": 160, "default_price": 400},
    "r200": {"name": "R-200",     "tipe": "BS/Reject", "stems_per_ikat": 200, "default_price": 350},
}

NORMAL_GRADES = ["g60", "g80", "g100", "g120", "g160"]
BS_GRADES     = ["r80", "r100", "r160", "r200"]
WARNA_OPTIONS = ["Putih", "Pink", "Kuning"]


class GradeInput(BaseModel):
    """Input per grade: key + jumlah ikat + harga per batang"""
    grade_key: str = Field(..., description="g60|g80|g100|g120|g160|r80|r100|r160|r200")
    jml_ikat: int = Field(0, ge=0, description="Jumlah ikat dipanen")
    harga_per_batang: int = Field(0, ge=0, description="Harga per batang (Rp)")


class WarnaGrading(BaseModel):
    """Grading input untuk satu warna varietas"""
    warna: str = Field(..., description="Putih | Pink | Kuning")
    bedengan: int = Field(0, ge=0, description="Jumlah bedengan varietas ini")
    grades: List[GradeInput] = Field(default_factory=list)


class HarvestRecordV2Create(BaseModel):
    """Full ikat-based harvest record dengan breakdown per warna & grade"""
    batch_id: str = Field(..., description="ID batch tanam")
    house_name: str = Field("House 1", description="Nama greenhouse / house")
    harvest_date: str = Field(..., json_schema_extra={"example": "2026-10-21"})
    varieties: List[WarnaGrading] = Field(..., description="Grading per warna: Putih, Pink, Kuning")
    biaya_operasional: int = Field(0, ge=0, description="Biaya operasional siklus (Rp)")
    biaya_penyusutan: int = Field(0, ge=0, description="Biaya penyusutan greenhouse/siklus (Rp)")
    harga_ekspektasi_per_btg: int = Field(1200, ge=0, description="Harga ekspektasi awal (Rp/btg)")
    notes: Optional[str] = None


class CostJournalCreate(BaseModel):
    """Input jurnal biaya harian operasional"""
    batch_id: str
    tanggal: str = Field(..., json_schema_extra={"example": "2026-08-15"})
    kategori: str = Field(..., description="Bibit|Pupuk|Pestisida|Tenaga Kerja|Listrik|Lain-lain")
    deskripsi: Optional[str] = Field(None, json_schema_extra={"example": "Beli NPK 50kg"})
    jumlah: int = Field(..., gt=0, description="Jumlah biaya (Rp)")
