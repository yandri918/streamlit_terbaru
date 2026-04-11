"""
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

# ============================================================================
# Base Response Models
# ============================================================================

class SuccessResponse(BaseModel):
    status: str = "success"
    data: Dict[str, Any]
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    status: str = "error"
    error: Dict[str, str]
    timestamp: datetime = Field(default_factory=datetime.now)

# ============================================================================
# Tax Calculation Request Models
# ============================================================================

class PPh21Request(BaseModel):
    gaji_pokok: float = Field(..., gt=0, description="Gaji pokok per bulan")
    tunjangan: float = Field(default=0, ge=0, description="Tunjangan tetap")
    bonus: float = Field(default=0, ge=0, description="Bonus")
    status_kawin: str = Field(..., pattern="^(TK|K)/[0-3]$", description="Status kawin (TK/0, K/1, dll)")
    user_name: Optional[str] = Field(default="API User", description="Nama pengguna")
    company_name: Optional[str] = Field(default="", description="Nama perusahaan")
    
    class Config:
        json_schema_extra = {
            "example": {
                "gaji_pokok": 10000000,
                "tunjangan": 2000000,
                "bonus": 0,
                "status_kawin": "K/1",
                "user_name": "John Doe",
                "company_name": "PT Example"
            }
        }

class PPh23Request(BaseModel):
    jenis_jasa: str = Field(..., description="Jenis jasa (Jasa Konsultan, Sewa, dll)")
    jumlah_bruto: float = Field(..., gt=0, description="Jumlah bruto")
    punya_npwp: bool = Field(default=True, description="Punya NPWP atau tidak")
    user_name: Optional[str] = Field(default="API User")
    company_name: Optional[str] = Field(default="")
    
    class Config:
        json_schema_extra = {
            "example": {
                "jenis_jasa": "Jasa Konsultan",
                "jumlah_bruto": 50000000,
                "punya_npwp": True,
                "user_name": "Jane Doe",
                "company_name": "PT Consulting"
            }
        }

class PPNRequest(BaseModel):
    harga_jual: float = Field(..., gt=0, description="Harga jual")
    termasuk_ppn: bool = Field(default=False, description="Harga sudah termasuk PPN")
    user_name: Optional[str] = Field(default="API User")
    company_name: Optional[str] = Field(default="")
    
    class Config:
        json_schema_extra = {
            "example": {
                "harga_jual": 100000000,
                "termasuk_ppn": False,
                "user_name": "Sales Manager",
                "company_name": "PT Trading"
            }
        }

class PPhBadanRequest(BaseModel):
    omzet: float = Field(..., gt=0, description="Omzet tahunan")
    biaya_operasional: float = Field(..., ge=0, description="Biaya operasional")
    koreksi_fiskal: float = Field(default=0, description="Koreksi fiskal")
    is_umkm: bool = Field(default=False, description="Eligible UMKM atau tidak")
    user_name: Optional[str] = Field(default="API User")
    company_name: Optional[str] = Field(default="")
    
    class Config:
        json_schema_extra = {
            "example": {
                "omzet": 5000000000,
                "biaya_operasional": 3000000000,
                "koreksi_fiskal": 100000000,
                "is_umkm": True,
                "user_name": "CFO",
                "company_name": "PT Maju Jaya"
            }
        }

class PBBRequest(BaseModel):
    njop_tanah: float = Field(..., gt=0, description="NJOP tanah")
    njop_bangunan: float = Field(..., ge=0, description="NJOP bangunan")
    njoptkp: float = Field(default=10000000, description="NJOPTKP")
    user_name: Optional[str] = Field(default="API User")
    company_name: Optional[str] = Field(default="")
    
    class Config:
        json_schema_extra = {
            "example": {
                "njop_tanah": 500000000,
                "njop_bangunan": 300000000,
                "njoptkp": 10000000,
                "user_name": "Property Owner",
                "company_name": "PT Property"
            }
        }

class PKBRequest(BaseModel):
    njkb: float = Field(..., gt=0, description="NJKB kendaraan")
    bobot: float = Field(default=1.0, ge=0, description="Bobot kendaraan")
    tarif_daerah: float = Field(default=0.02, ge=0, le=1, description="Tarif daerah (default 2%)")
    user_name: Optional[str] = Field(default="API User")
    company_name: Optional[str] = Field(default="")
    
    class Config:
        json_schema_extra = {
            "example": {
                "njkb": 200000000,
                "bobot": 1.0,
                "tarif_daerah": 0.02,
                "user_name": "Vehicle Owner",
                "company_name": "PT Transport"
            }
        }

class BPHTBRequest(BaseModel):
    npop: float = Field(..., gt=0, description="NPOP (Nilai Perolehan Objek Pajak)")
    npoptkp: float = Field(default=60000000, description="NPOPTKP")
    tarif: float = Field(default=0.05, ge=0, le=1, description="Tarif BPHTB (default 5%)")
    user_name: Optional[str] = Field(default="API User")
    company_name: Optional[str] = Field(default="")
    
    class Config:
        json_schema_extra = {
            "example": {
                "npop": 500000000,
                "npoptkp": 60000000,
                "tarif": 0.05,
                "user_name": "Property Buyer",
                "company_name": "PT Real Estate"
            }
        }

# ============================================================================
# Dashboard Request Models
# ============================================================================

class DashboardSummaryRequest(BaseModel):
    start_date: Optional[str] = Field(default=None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(default=None, description="End date (YYYY-MM-DD)")
    data_source: str = Field(default="sample", description="Data source: sample, audit_trail, database")

# ============================================================================
# AI Advisor Request Models
# ============================================================================

class AIAdvisorRequest(BaseModel):
    question: str = Field(..., min_length=5, description="Tax question")
    context: Optional[Dict[str, Any]] = Field(default=None, description="User context (omzet, biaya, etc)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "Bagaimana cara menurunkan PPh Badan 2025?",
                "context": {
                    "omzet": 5000000000,
                    "biaya_produksi": 3000000000
                }
            }
        }

# ============================================================================
# Report Generation Request Models
# ============================================================================

class ReportGenerateRequest(BaseModel):
    calc_type: str = Field(..., description="Calculation type")
    user_name: str = Field(..., description="User name")
    company_name: str = Field(..., description="Company name")
    input_data: Dict[str, Any] = Field(..., description="Input data")
    output_data: Dict[str, Any] = Field(..., description="Output data")

# ============================================================================
# Webhook Request Models
# ============================================================================

class WebhookRegisterRequest(BaseModel):
    event: str = Field(..., description="Event type (calculation.completed, etc)")
    url: str = Field(..., description="Webhook callback URL")
    secret: str = Field(..., min_length=10, description="Webhook secret key")
    
    class Config:
        json_schema_extra = {
            "example": {
                "event": "calculation.completed",
                "url": "https://your-erp.com/webhooks/taxpro",
                "secret": "webhook-secret-key-12345"
            }
        }
