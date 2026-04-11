"""
Tax Calculator Module for API
Contains calculation functions for all tax types
"""

# ============================================================================
# PPh 21 Calculation
# ============================================================================

def calculate_pph21_api(gaji_pokok: float, tunjangan: float = 0, bonus: float = 0, status_kawin: str = "TK/0"):
    """Calculate PPh 21 for API"""
    
    # PTKP values
    ptkp_values = {
        "TK/0": 54000000,
        "TK/1": 58500000,
        "TK/2": 63000000,
        "TK/3": 67500000,
        "K/0": 58500000,
        "K/1": 63000000,
        "K/2": 67500000,
        "K/3": 72000000
    }
    
    # Calculate
    penghasilan_bruto = gaji_pokok + tunjangan + bonus
    biaya_jabatan = min(penghasilan_bruto * 0.05, 500000)
    penghasilan_netto_bulanan = penghasilan_bruto - biaya_jabatan
    penghasilan_netto_tahunan = penghasilan_netto_bulanan * 12
    
    ptkp = ptkp_values.get(status_kawin, 54000000)
    pkp = max(penghasilan_netto_tahunan - ptkp, 0)
    
    # Progressive tax rates
    pajak_tahunan = 0
    if pkp > 0:
        if pkp <= 60000000:
            pajak_tahunan = pkp * 0.05
        elif pkp <= 250000000:
            pajak_tahunan = (60000000 * 0.05) + ((pkp - 60000000) * 0.15)
        elif pkp <= 500000000:
            pajak_tahunan = (60000000 * 0.05) + (190000000 * 0.15) + ((pkp - 250000000) * 0.25)
        else:
            pajak_tahunan = (60000000 * 0.05) + (190000000 * 0.15) + (250000000 * 0.25) + ((pkp - 500000000) * 0.30)
    
    pajak_bulanan = pajak_tahunan / 12
    
    return {
        "penghasilan_bruto": penghasilan_bruto,
        "biaya_jabatan": biaya_jabatan,
        "penghasilan_netto": penghasilan_netto_tahunan,
        "ptkp": ptkp,
        "pkp": pkp,
        "pajak_bulanan": pajak_bulanan,
        "pajak_tahunan": pajak_tahunan
    }

# ============================================================================
# PPh 23 Calculation
# ============================================================================

def calculate_pph23_api(jenis_jasa: str, jumlah_bruto: float, punya_npwp: bool = True):
    """Calculate PPh 23 for API"""
    
    # Tarif based on service type
    tarif_map = {
        "Jasa Konsultan": 0.02,
        "Jasa Manajemen": 0.02,
        "Sewa": 0.02,
        "Royalti": 0.15,
        "Hadiah": 0.15,
        "Bunga": 0.15
    }
    
    tarif = tarif_map.get(jenis_jasa, 0.02)
    
    # Double tarif if no NPWP
    if not punya_npwp:
        tarif = tarif * 2
    
    pph23 = jumlah_bruto * tarif
    jumlah_diterima = jumlah_bruto - pph23
    
    return {
        "jumlah_bruto": jumlah_bruto,
        "tarif": tarif,
        "pph23": pph23,
        "jumlah_diterima": jumlah_diterima,
        "punya_npwp": punya_npwp
    }

# ============================================================================
# PPN Calculation
# ============================================================================

def calculate_ppn_api(harga_jual: float, termasuk_ppn: bool = False):
    """Calculate PPN for API"""
    
    tarif_ppn = 0.11  # 11%
    
    if termasuk_ppn:
        # Harga sudah termasuk PPN
        dpp = harga_jual / (1 + tarif_ppn)
        ppn = dpp * tarif_ppn
        harga_jual_final = harga_jual
    else:
        # Harga belum termasuk PPN
        dpp = harga_jual
        ppn = dpp * tarif_ppn
        harga_jual_final = dpp + ppn
    
    return {
        "dpp": dpp,
        "ppn": ppn,
        "harga_jual": harga_jual_final,
        "tarif": tarif_ppn
    }

# ============================================================================
# PPh Badan Calculation
# ============================================================================

def calculate_pph_badan_api(omzet: float, biaya_operasional: float, koreksi_fiskal: float = 0, is_umkm: bool = False):
    """Calculate PPh Badan for API"""
    
    laba_kotor = omzet - biaya_operasional
    pkp = laba_kotor + koreksi_fiskal
    
    # Check UMKM eligibility
    threshold_umkm = 4800000000  # 4.8 Billion
    eligible_umkm = omzet < threshold_umkm
    
    if is_umkm and eligible_umkm:
        # UMKM: 0.5% final tax
        pph_badan = omzet * 0.005
        tarif_display = "0.5% (UMKM Final)"
    else:
        # Non-UMKM: 22% of PKP
        pph_badan = pkp * 0.22
        tarif_display = "22% (Non-UMKM)"
    
    return {
        "omzet": omzet,
        "laba_kotor": laba_kotor,
        "koreksi_fiskal": koreksi_fiskal,
        "pkp": pkp,
        "pph_badan": pph_badan,
        "tarif": tarif_display,
        "eligible_umkm": eligible_umkm,
        "is_umkm": is_umkm
    }

# ============================================================================
# PBB Calculation
# ============================================================================

def calculate_pbb_api(njop_tanah: float, njop_bangunan: float, njoptkp: float = 10000000):
    """Calculate PBB for API"""
    
    njop_total = njop_tanah + njop_bangunan
    njop_kena_pajak = max(njop_total - njoptkp, 0)
    njkp = njop_kena_pajak * 0.20  # 20% of taxable NJOP
    pbb = njkp * 0.005  # 0.5% tax rate
    
    return {
        "njop_tanah": njop_tanah,
        "njop_bangunan": njop_bangunan,
        "njop_total": njop_total,
        "njoptkp": njoptkp,
        "njop_kena_pajak": njop_kena_pajak,
        "njkp": njkp,
        "pbb": pbb
    }

# ============================================================================
# PKB Calculation
# ============================================================================

def calculate_pkb_api(njkb: float, bobot: float = 1.0, tarif_daerah: float = 0.02):
    """Calculate PKB for API"""
    
    pkb = njkb * bobot * tarif_daerah
    swdkllj = 143000  # Standard SWDKLLJ fee
    total = pkb + swdkllj
    
    return {
        "njkb": njkb,
        "bobot": bobot,
        "tarif_daerah": tarif_daerah,
        "pkb": pkb,
        "swdkllj": swdkllj,
        "total": total
    }

# ============================================================================
# BPHTB Calculation
# ============================================================================

def calculate_bphtb_api(npop: float, npoptkp: float = 60000000, tarif: float = 0.05):
    """Calculate BPHTB for API"""
    
    npop_kena_pajak = max(npop - npoptkp, 0)
    bphtb = npop_kena_pajak * tarif
    
    return {
        "npop": npop,
        "npoptkp": npoptkp,
        "npop_kena_pajak": npop_kena_pajak,
        "tarif": tarif,
        "bphtb": bphtb
    }
