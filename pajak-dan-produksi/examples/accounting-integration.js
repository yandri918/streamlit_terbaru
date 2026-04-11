/**
 * TaxPro API SDK for Accounting Software Integration
 * Example: Accurate, Zahir, or custom accounting systems
 */

const axios = require('axios');

class TaxProSDK {
    /**
     * Initialize TaxPro SDK
     * @param {string} apiKey - API key for authentication
     * @param {string} baseURL - Base URL of API (default: http://localhost:8000)
     */
    constructor(apiKey, baseURL = 'http://localhost:8000') {
        this.apiKey = apiKey;
        this.baseURL = baseURL;
        this.client = axios.create({
            baseURL: this.baseURL,
            headers: {
                'X-API-Key': this.apiKey,
                'Content-Type': 'application/json'
            }
        });
    }

    /**
     * Calculate PPh 21 (Employee Tax)
     */
    async calculatePPh21(data) {
        const response = await this.client.post('/api/v1/tax/pph21', data);
        return response.data;
    }

    /**
     * Calculate PPh 23 (Withholding Tax)
     */
    async calculatePPh23(data) {
        const response = await this.client.post('/api/v1/tax/pph23', data);
        return response.data;
    }

    /**
     * Calculate PPN (VAT)
     */
    async calculatePPN(data) {
        const response = await this.client.post('/api/v1/tax/ppn', data);
        return response.data;
    }

    /**
     * Calculate PPh Badan (Corporate Tax)
     */
    async calculatePPhBadan(data) {
        const response = await this.client.post('/api/v1/tax/pph-badan', data);
        return response.data;
    }

    /**
     * Get Dashboard Summary
     */
    async getDashboardSummary(startDate, endDate) {
        const response = await this.client.get('/api/v1/dashboard/summary', {
            params: { start_date: startDate, end_date: endDate }
        });
        return response.data;
    }

    /**
     * Ask AI Tax Advisor
     */
    async askAIAdvisor(question, context = null) {
        const response = await this.client.post('/api/v1/ai/advisor', {
            question,
            context
        });
        return response.data;
    }

    /**
     * Generate PDF Report
     */
    async generateReport(data) {
        const response = await this.client.post('/api/v1/reports/generate', data);
        return response.data;
    }
}

// ============================================================================
// Example Usage in Accounting Software
// ============================================================================

async function main() {
    console.log('=== TaxPro API - Accounting Software Integration ===\n');

    // Initialize SDK
    const taxpro = new TaxProSDK('demo-key-12345');

    try {
        // 1. Calculate employee payroll tax
        console.log('1. Calculating PPh 21 for payroll...');
        const pph21 = await taxpro.calculatePPh21({
            gaji_pokok: 10000000,
            tunjangan: 2000000,
            status_kawin: 'K/1'
        });
        console.log(`   ✓ PPh 21: Rp ${pph21.data.pajak_bulanan.toLocaleString('id-ID')}\n`);

        // 2. Calculate withholding tax for vendor payment
        console.log('2. Calculating PPh 23 for vendor payment...');
        const pph23 = await taxpro.calculatePPh23({
            jenis_jasa: 'Jasa Konsultan',
            jumlah_bruto: 50000000,
            punya_npwp: true
        });
        console.log(`   ✓ PPh 23: Rp ${pph23.data.pph23.toLocaleString('id-ID')}\n`);

        // 3. Calculate VAT for sales invoice
        console.log('3. Calculating PPN for sales invoice...');
        const ppn = await taxpro.calculatePPN({
            harga_jual: 100000000,
            termasuk_ppn: false
        });
        console.log(`   ✓ PPN: Rp ${ppn.data.ppn.toLocaleString('id-ID')}`);
        console.log(`   ✓ Total: Rp ${ppn.data.harga_jual.toLocaleString('id-ID')}\n`);

        // 4. Calculate corporate tax
        console.log('4. Calculating PPh Badan...');
        const pphBadan = await taxpro.calculatePPhBadan({
            omzet: 5000000000,
            biaya_operasional: 3000000000,
            is_umkm: true
        });
        console.log(`   ✓ PPh Badan: Rp ${pphBadan.data.pph_badan.toLocaleString('id-ID')}`);
        console.log(`   ✓ Tarif: ${pphBadan.data.tarif}\n`);

        // 5. Get dashboard for financial reporting
        console.log('5. Getting dashboard summary...');
        const dashboard = await taxpro.getDashboardSummary('2024-01-01', '2024-12-31');
        console.log(`   ✓ Total Tax YTD: Rp ${dashboard.data.total_tax_ytd.toLocaleString('id-ID')}`);
        console.log(`   ✓ Tax Efficiency: ${dashboard.data.tax_efficiency}%\n`);

        // 6. Ask AI for tax advice
        console.log('6. Asking AI advisor...');
        const aiResponse = await taxpro.askAIAdvisor(
            'Bagaimana cara mengoptimalkan pajak perusahaan?',
            { omzet: 5000000000 }
        );
        console.log(`   ✓ AI Response: ${aiResponse.data.answer.substring(0, 150)}...\n`);

        console.log('=== Integration Complete ===');

    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }
}

// Run example
if (require.main === module) {
    main();
}

module.exports = TaxProSDK;
