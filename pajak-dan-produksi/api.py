"""
TaxPro Indonesia - FastAPI Backend
RESTful API for tax calculations and analytics
"""

from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
# Import models
from api_models import *

# Import calculation functions
from tax_calculator import (
    calculate_pph21_api, calculate_pph23_api, calculate_ppn_api,
    calculate_pph_badan_api, calculate_pbb_api, calculate_pkb_api,
    calculate_bphtb_api
)

# Import other services
from ai_tax_advisor import get_ai_response

# Conditional import for PDF generator (reportlab might fail on Vercel)
try:
    from pdf_generator import generate_tax_report_pdf
    PDF_GENERATOR_AVAILABLE = True
except ImportError:
    PDF_GENERATOR_AVAILABLE = False
    print("Warning: PDF generator not available (reportlab missing/failed)")

# Conditional import for dashboard data (heavy dependencies)
try:
    import pandas as pd
    from cfo_dashboard_data import (
        load_from_audit_trail, generate_sample_tax_data,
        process_tax_data_for_dashboard
    )
    DASHBOARD_AVAILABLE = True
except ImportError:
    DASHBOARD_AVAILABLE = False
    print("Warning: Dashboard module not available (pandas/numpy missing)")

# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="TaxPro Indonesia API",
    description="RESTful API for Indonesian tax calculations and analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ============================================================================
# CORS Configuration
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production: ["https://your-domain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Authentication
# ============================================================================

# In production, store API keys in database or environment variables
VALID_API_KEYS = {
    "demo-key-12345": "Demo User",
    "prod-key-67890": "Production User"
}

async def verify_api_key(x_api_key: str = Header(..., description="API Key for authentication")):
    """Verify API key from header"""
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return VALID_API_KEYS[x_api_key]

# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """API root endpoint"""
    return {
        "message": "TaxPro Indonesia API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# Tax Calculation Endpoints
# ============================================================================

@app.post("/api/v1/tax/pph21", 
          response_model=SuccessResponse,
          tags=["Tax Calculations"],
          summary="Calculate PPh 21 (Employee Tax)",
          dependencies=[Depends(verify_api_key)])
async def api_calculate_pph21(request: PPh21Request):
    """
    Calculate PPh 21 (Pajak Penghasilan Pasal 21) - Employee Income Tax
    
    - **gaji_pokok**: Monthly base salary
    - **tunjangan**: Fixed allowances
    - **bonus**: Bonus amount
    - **status_kawin**: Marital status (TK/0, K/1, K/2, K/3)
    """
    try:
        result = calculate_pph21_api(
            gaji_pokok=request.gaji_pokok,
            tunjangan=request.tunjangan,
            bonus=request.bonus,
            status_kawin=request.status_kawin
        )
        
        return SuccessResponse(
            data=result,
            message="PPh 21 calculated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/tax/pph23",
          response_model=SuccessResponse,
          tags=["Tax Calculations"],
          summary="Calculate PPh 23 (Withholding Tax)",
          dependencies=[Depends(verify_api_key)])
async def api_calculate_pph23(request: PPh23Request):
    """
    Calculate PPh 23 (Pajak Penghasilan Pasal 23) - Withholding Tax
    
    - **jenis_jasa**: Service type (Consulting, Rent, etc.)
    - **jumlah_bruto**: Gross amount
    - **punya_npwp**: Has NPWP or not
    """
    try:
        result = calculate_pph23_api(
            jenis_jasa=request.jenis_jasa,
            jumlah_bruto=request.jumlah_bruto,
            punya_npwp=request.punya_npwp
        )
        
        return SuccessResponse(
            data=result,
            message="PPh 23 calculated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/tax/ppn",
          response_model=SuccessResponse,
          tags=["Tax Calculations"],
          summary="Calculate PPN (VAT)",
          dependencies=[Depends(verify_api_key)])
async def api_calculate_ppn(request: PPNRequest):
    """
    Calculate PPN (Pajak Pertambahan Nilai) - Value Added Tax
    
    - **harga_jual**: Selling price
    - **termasuk_ppn**: Price includes VAT or not
    """
    try:
        result = calculate_ppn_api(
            harga_jual=request.harga_jual,
            termasuk_ppn=request.termasuk_ppn
        )
        
        return SuccessResponse(
            data=result,
            message="PPN calculated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/tax/pph-badan",
          response_model=SuccessResponse,
          tags=["Tax Calculations"],
          summary="Calculate PPh Badan (Corporate Tax)",
          dependencies=[Depends(verify_api_key)])
async def api_calculate_pph_badan(request: PPhBadanRequest):
    """
    Calculate PPh Badan (Pajak Penghasilan Badan) - Corporate Income Tax
    
    - **omzet**: Annual revenue
    - **biaya_operasional**: Operating expenses
    - **koreksi_fiskal**: Fiscal corrections
    - **is_umkm**: UMKM eligible or not
    """
    try:
        result = calculate_pph_badan_api(
            omzet=request.omzet,
            biaya_operasional=request.biaya_operasional,
            koreksi_fiskal=request.koreksi_fiskal,
            is_umkm=request.is_umkm
        )
        
        return SuccessResponse(
            data=result,
            message="PPh Badan calculated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/tax/pbb",
          response_model=SuccessResponse,
          tags=["Tax Calculations"],
          summary="Calculate PBB (Property Tax)",
          dependencies=[Depends(verify_api_key)])
async def api_calculate_pbb(request: PBBRequest):
    """
    Calculate PBB (Pajak Bumi dan Bangunan) - Land and Building Tax
    
    - **njop_tanah**: Land NJOP value
    - **njop_bangunan**: Building NJOP value
    - **njoptkp**: NJOPTKP deduction
    """
    try:
        result = calculate_pbb_api(
            njop_tanah=request.njop_tanah,
            njop_bangunan=request.njop_bangunan,
            njoptkp=request.njoptkp
        )
        
        return SuccessResponse(
            data=result,
            message="PBB calculated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/tax/pkb",
          response_model=SuccessResponse,
          tags=["Tax Calculations"],
          summary="Calculate PKB (Vehicle Tax)",
          dependencies=[Depends(verify_api_key)])
async def api_calculate_pkb(request: PKBRequest):
    """
    Calculate PKB (Pajak Kendaraan Bermotor) - Motor Vehicle Tax
    
    - **njkb**: Vehicle NJKB value
    - **bobot**: Vehicle weight factor
    - **tarif_daerah**: Regional tax rate
    """
    try:
        result = calculate_pkb_api(
            njkb=request.njkb,
            bobot=request.bobot,
            tarif_daerah=request.tarif_daerah
        )
        
        return SuccessResponse(
            data=result,
            message="PKB calculated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/tax/bphtb",
          response_model=SuccessResponse,
          tags=["Tax Calculations"],
          summary="Calculate BPHTB (Land Transfer Tax)",
          dependencies=[Depends(verify_api_key)])
async def api_calculate_bphtb(request: BPHTBRequest):
    """
    Calculate BPHTB (Bea Perolehan Hak atas Tanah dan Bangunan) - Land Transfer Tax
    
    - **npop**: NPOP value
    - **npoptkp**: NPOPTKP deduction
    - **tarif**: BPHTB tax rate
    """
    try:
        result = calculate_bphtb_api(
            npop=request.npop,
            npoptkp=request.npoptkp,
            tarif=request.tarif
        )
        
        return SuccessResponse(
            data=result,
            message="BPHTB calculated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# Dashboard & Analytics Endpoints
# ============================================================================

@app.get("/api/v1/dashboard/summary",
         response_model=SuccessResponse,
         tags=["Dashboard & Analytics"],
         summary="Get Dashboard KPI Summary",
         dependencies=[Depends(verify_api_key)])
async def get_dashboard_summary(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    data_source: str = "sample"
):
    """
    Get dashboard KPI summary
    
    - **start_date**: Start date (YYYY-MM-DD)
    - **end_date**: End date (YYYY-MM-DD)
    - **data_source**: Data source (sample, audit_trail, database)
    """
    try:
        if not DASHBOARD_AVAILABLE:
            return SuccessResponse(
                data={
                    "total_tax_ytd": 0,
                    "pph21_ytd": 0,
                    "pph_badan_ytd": 0,
                    "tax_efficiency": 0,
                    "period": {"start": start_date, "end": end_date},
                    "note": "Dashboard analytics unavailable in this environment"
                },
                message="Dashboard module not available"
            )

        # Load data based on source
        if data_source == "audit_trail":
            raw_data = load_from_audit_trail()
            if raw_data is not None:
                tax_data = process_tax_data_for_dashboard(raw_data)
            else:
                tax_data = generate_sample_tax_data()
        else:
            tax_data = generate_sample_tax_data()
        
        # Calculate KPIs
        total_tax = tax_data['amount'].sum()
        pph21_ytd = tax_data[tax_data['tax_type'] == 'PPh 21']['amount'].sum()
        pph_badan_ytd = tax_data[tax_data['tax_type'] == 'PPh Badan']['amount'].sum()
        
        summary = {
            "total_tax_ytd": float(total_tax),
            "pph21_ytd": float(pph21_ytd),
            "pph_badan_ytd": float(pph_badan_ytd),
            "tax_efficiency": 85.5,
            "period": {
                "start": start_date or "2024-01-01",
                "end": end_date or "2024-12-31"
            }
        }
        
        return SuccessResponse(
            data=summary,
            message="Dashboard summary retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# AI Advisor Endpoint
# ============================================================================

@app.post("/api/v1/ai/advisor",
          response_model=SuccessResponse,
          tags=["AI & Insights"],
          summary="Chat with AI Tax Advisor",
          dependencies=[Depends(verify_api_key)])
async def ai_tax_advisor(request: AIAdvisorRequest):
    """
    Get tax advice from AI advisor
    
    - **question**: Tax question
    - **context**: User context (optional)
    """
    try:
        response = get_ai_response(request.question, request.context)
        
        return SuccessResponse(
            data={
                "answer": response,
                "question": request.question
            },
            message="AI response generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Report Generation Endpoint
# ============================================================================

@app.post("/api/v1/reports/generate",
          tags=["Reports"],
          summary="Generate PDF Tax Report",
          dependencies=[Depends(verify_api_key)])
async def generate_report(request: ReportGenerateRequest):
    """
    Generate PDF tax report
    
    Returns base64 encoded PDF
    """
    try:
        if not PDF_GENERATOR_AVAILABLE:
            raise HTTPException(status_code=503, detail="PDF generation service not available in this environment")

        pdf_bytes = generate_tax_report_pdf(
            calc_type=request.calc_type,
            user_name=request.user_name,
            company_name=request.company_name,
            input_data=request.input_data,
            output_data=request.output_data
        )
        
        import base64
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        return {
            "status": "success",
            "data": {
                "pdf_base64": pdf_base64,
                "filename": f"Tax_Report_{request.calc_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            },
            "message": "Report generated successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            },
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error": {
                "code": 500,
                "message": "Internal Server Error: " + str(exc)
            },
            "timestamp": datetime.now().isoformat()
        }
    )

# ============================================================================
# Run Server
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
