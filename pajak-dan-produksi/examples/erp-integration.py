"""
TaxPro API Client for ERP Integration
Example: SAP, Odoo, or custom ERP systems
"""

import requests
from typing import Dict, Any, Optional
from datetime import datetime

class TaxProClient:
    """
    TaxPro Indonesia API Client for ERP Integration
    
    Usage:
        client = TaxProClient(api_key="your-api-key")
        result = client.calculate_pph_badan(omzet=5000000000, biaya=3000000000)
    """
    
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to API"""
        url = f"{self.base_url}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, headers=self.headers, params=data)
        else:
            response = requests.post(url, headers=self.headers, json=data)
        
        response.raise_for_status()
        return response.json()
    
    # Tax Calculation Methods
    
    def calculate_pph21(self, gaji_pokok: float, tunjangan: float = 0, 
                       status_kawin: str = "TK/0") -> Dict[str, Any]:
        """Calculate PPh 21 (Employee Tax)"""
        return self._make_request("POST", "/api/v1/tax/pph21", {
            "gaji_pokok": gaji_pokok,
            "tunjangan": tunjangan,
            "status_kawin": status_kawin
        })
    
    def calculate_pph_badan(self, omzet: float, biaya_operasional: float,
                           koreksi_fiskal: float = 0, is_umkm: bool = False) -> Dict[str, Any]:
        """Calculate PPh Badan (Corporate Tax)"""
        return self._make_request("POST", "/api/v1/tax/pph-badan", {
            "omzet": omzet,
            "biaya_operasional": biaya_operasional,
            "koreksi_fiskal": koreksi_fiskal,
            "is_umkm": is_umkm
        })
    
    def calculate_ppn(self, harga_jual: float, termasuk_ppn: bool = False) -> Dict[str, Any]:
        """Calculate PPN (VAT)"""
        return self._make_request("POST", "/api/v1/tax/ppn", {
            "harga_jual": harga_jual,
            "termasuk_ppn": termasuk_ppn
        })
    
    # Dashboard Methods
    
    def get_dashboard_summary(self, start_date: Optional[str] = None,
                             end_date: Optional[str] = None) -> Dict[str, Any]:
        """Get dashboard KPI summary"""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        return self._make_request("GET", "/api/v1/dashboard/summary", params)
    
    # AI Methods
    
    def ask_ai_advisor(self, question: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Ask AI tax advisor"""
        return self._make_request("POST", "/api/v1/ai/advisor", {
            "question": question,
            "context": context
        })


# ============================================================================
# Example Usage in ERP System
# ============================================================================

def main():
    """Example ERP integration workflow"""
    
    # Initialize client
    client = TaxProClient(api_key="demo-key-12345")
    
    print("=== TaxPro API - ERP Integration Example ===\n")
    
    # 1. Calculate employee payroll tax
    print("1. Calculating PPh 21 for employee payroll...")
    pph21_result = client.calculate_pph21(
        gaji_pokok=10000000,
        tunjangan=2000000,
        status_kawin="K/1"
    )
    
    if pph21_result["status"] == "success":
        pajak = pph21_result["data"]["pajak_bulanan"]
        print(f"   ✓ PPh 21 Bulanan: Rp {pajak:,.0f}\n")
    
    # 2. Calculate corporate tax
    print("2. Calculating PPh Badan for company...")
    pph_badan_result = client.calculate_pph_badan(
        omzet=5000000000,
        biaya_operasional=3000000000,
        is_umkm=True
    )
    
    if pph_badan_result["status"] == "success":
        pajak = pph_badan_result["data"]["pph_badan"]
        tarif = pph_badan_result["data"]["tarif"]
        print(f"   ✓ PPh Badan: Rp {pajak:,.0f} ({tarif})\n")
    
    # 3. Calculate VAT for sales
    print("3. Calculating PPN for sales transaction...")
    ppn_result = client.calculate_ppn(
        harga_jual=100000000,
        termasuk_ppn=False
    )
    
    if ppn_result["status"] == "success":
        ppn = ppn_result["data"]["ppn"]
        total = ppn_result["data"]["harga_jual"]
        print(f"   ✓ PPN: Rp {ppn:,.0f}")
        print(f"   ✓ Total: Rp {total:,.0f}\n")
    
    # 4. Get dashboard summary for CFO reporting
    print("4. Getting dashboard summary for CFO...")
    dashboard = client.get_dashboard_summary(
        start_date="2024-01-01",
        end_date="2024-12-31"
    )
    
    if dashboard["status"] == "success":
        total_tax = dashboard["data"]["total_tax_ytd"]
        efficiency = dashboard["data"]["tax_efficiency"]
        print(f"   ✓ Total Tax YTD: Rp {total_tax:,.0f}")
        print(f"   ✓ Tax Efficiency: {efficiency}%\n")
    
    # 5. Ask AI for tax optimization advice
    print("5. Asking AI advisor for tax optimization...")
    ai_response = client.ask_ai_advisor(
        question="Bagaimana cara menurunkan PPh Badan?",
        context={"omzet": 5000000000}
    )
    
    if ai_response["status"] == "success":
        answer = ai_response["data"]["answer"]
        print(f"   ✓ AI Response:\n{answer[:200]}...\n")
    
    print("=== Integration Complete ===")


if __name__ == "__main__":
    main()
