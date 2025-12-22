"""Build enhanced Harvest Database HTML with cost tracking and profitability."""

# Due to size, I'll update the existing file by inserting cost tracking sections
import re

with open('templates/modules/harvest_database.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add cost input section to the form (after commodity/date row, before criteria section)
cost_section_html = '''
                <div class="form-row">
                    <div class="form-group">
                        <label>Cuaca</label>
                        <select id="weather">
                            <option value="">Pilih Cuaca</option>
                            <option value="☀️">☀️ Cerah</option>
                            <option value="🌤️">🌤️ Berawan</option>
                            <option value="🌧️">🌧️ Hujan</option>
                            <option value="⛈️">⛈️ Badai</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Catatan</label>
                        <input type="text" id="notes" placeholder="Catatan tambahan (opsional)">
                    </div>
                </div>

                <div class="criteria-section" style="background: #fff3cd; border: 2px solid #ffc107; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h3 style="color: #856404; margin-bottom: 15px;">💰 Biaya Produksi</h3>
                    <p style="color: #856404; font-size: 0.9rem; margin-bottom: 15px;">Input biaya untuk menghitung profit otomatis</p>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Bibit/Benih (Rp)</label>
                            <input type="number" id="cost-bibit" class="cost-input" min="0" step="1000" value="0" onchange="calculateCosts()">
                        </div>
                        <div class="form-group">
                            <label>Pupuk (Rp)</label>
                            <input type="number" id="cost-pupuk" class="cost-input" min="0" step="1000" value="0" onchange="calculateCosts()">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Pestisida (Rp)</label>
                            <input type="number" id="cost-pestisida" class="cost-input" min="0" step="1000" value="0" onchange="calculateCosts()">
                        </div>
                        <div class="form-group">
                            <label>Tenaga Kerja (Rp)</label>
                            <input type="number" id="cost-tenaga-kerja" class="cost-input" min="0" step="1000" value="0" onchange="calculateCosts()">
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Lainnya (Rp)</label>
                        <input type="number" id="cost-lainnya" class="cost-input" min="0" step="1000" value="0" onchange="calculateCosts()">
                    </div>
                    
                    <div style="background: white; padding: 15px; border-radius: 8px; margin-top: 15px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <strong style="color: #2d3748;">Total Biaya:</strong>
                            <span id="total-cost-display" style="font-size: 1.3rem; font-weight: bold; color: #ef4444;">Rp 0</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 10px; border-top: 1px solid #e2e8f0;">
                            <strong style="color: #2d3748;">Estimasi Profit:</strong>
                            <span id="profit-preview" style="font-size: 1.3rem; font-weight: bold; color: #10b981;">Rp 0</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 5px; font-size: 0.9rem;">
                            <span style="color: #718096;">Margin:</span>
                            <span id="margin-preview" style="font-weight: 600; color: #3b82f6;">0%</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 5px; font-size: 0.9rem;">
                            <span style="color: #718096;">ROI:</span>
                            <span id="roi-preview" style="font-weight: 600; color: #8b5cf6;">0%</span>
                        </div>
                    </div>
                </div>
'''

# Insert cost section before criteria section
content = content.replace(
    '<div class="criteria-section">',
    cost_section_html + '\n                <div class="criteria-section">'
)

# 2. Add calculateCosts function to JavaScript
calculate_costs_js = '''
        // ========== COST CALCULATION ==========
        
        function calculateCosts() {
            const bibit = parseFloat(document.getElementById('cost-bibit').value) || 0;
            const pupuk = parseFloat(document.getElementById('cost-pupuk').value) || 0;
            const pestisida = parseFloat(document.getElementById('cost-pestisida').value) || 0;
            const tenagaKerja = parseFloat(document.getElementById('cost-tenaga-kerja').value) || 0;
            const lainnya = parseFloat(document.getElementById('cost-lainnya').value) || 0;
            
            const totalCost = bibit + pupuk + pestisida + tenagaKerja + lainnya;
            
            document.getElementById('total-cost-display').textContent = 
                'Rp ' + totalCost.toLocaleString('id-ID');
            
            // Calculate profit preview
            const totalRevenue = calculateTotalRevenue();
            const profit = totalRevenue - totalCost;
            const profitMargin = totalRevenue > 0 ? (profit / totalRevenue) * 100 : 0;
            const roi = totalCost > 0 ? (profit / totalCost) * 100 : 0;
            
            // Update previews with color coding
            const profitEl = document.getElementById('profit-preview');
            profitEl.textContent = 'Rp ' + profit.toLocaleString('id-ID');
            profitEl.style.color = profit >= 0 ? '#10b981' : '#ef4444';
            
            document.getElementById('margin-preview').textContent = profitMargin.toFixed(2) + '%';
            document.getElementById('roi-preview').textContent = roi.toFixed(2) + '%';
        }
        
        function calculateTotalRevenue() {
            const criteriaElements = document.querySelectorAll('.criteria-item');
            let totalRevenue = 0;
            
            criteriaElements.forEach(el => {
                const quantity = parseFloat(el.querySelector('.criterion-quantity')?.value) || 0;
                const price = parseFloat(el.querySelector('.criterion-price')?.value) || 0;
                totalRevenue += quantity * price;
            });
            
            return totalRevenue;
        }
'''

# Insert before submitRecord function
content = content.replace(
    '        async function submitRecord(event) {',
    calculate_costs_js + '\n        async function submitRecord(event) {'
)

# 3. Update submitRecord to include costs
submit_update = '''
            const recordData = {
                farmer_name: document.getElementById('farmer-name').value,
                farmer_phone: document.getElementById('farmer-phone').value,
                commodity: document.getElementById('commodity').value,
                location: document.getElementById('location').value,
                harvest_date: document.getElementById('harvest-date').value,
                criteria: criteria,
                costs: {
                    bibit: parseFloat(document.getElementById('cost-bibit').value) || 0,
                    pupuk: parseFloat(document.getElementById('cost-pupuk').value) || 0,
                    pestisida: parseFloat(document.getElementById('cost-pestisida').value) || 0,
                    tenaga_kerja: parseFloat(document.getElementById('cost-tenaga-kerja').value) || 0,
                    lainnya: parseFloat(document.getElementById('cost-lainnya').value) || 0
                },
                notes: document.getElementById('notes').value,
                weather: document.getElementById('weather').value
            };'''

content = re.sub(
    r'const recordData = \{[^}]+\};',
    submit_update,
    content,
    count=1
)

# 4. Update table display to show profit
table_update = '''
                    <thead>
                        <tr>
                            <th>Tanggal</th>
                            <th>Komoditas</th>
                            <th>Lokasi</th>
                            <th>Total (kg)</th>
                            <th>Nilai (Rp)</th>
                            <th>Biaya (Rp)</th>
                            <th>Profit (Rp)</th>
                            <th>Margin</th>
                            <th>Aksi</th>
                        </tr>
                    </thead>'''

content = content.replace(
    '''                    <thead>
                        <tr>
                            <th>Tanggal</th>
                            <th>Komoditas</th>
                            <th>Lokasi</th>
                            <th>Total (kg)</th>
                            <th>Nilai (Rp)</th>
                            <th>Aksi</th>
                        </tr>
                    </thead>''',
    table_update
)

# 5. Update table row display
row_update = '''
                    <tr onclick="toggleDetails('${record.id}')" style="cursor: pointer;">
                        <td>${record.harvest_date}</td>
                        <td>${record.weather ? record.weather + ' ' : ''}${record.commodity}</td>
                        <td>${record.location}</td>
                        <td>${record.total_quantity} kg</td>
                        <td>Rp ${record.total_value.toLocaleString('id-ID')}</td>
                        <td>Rp ${(record.total_cost || 0).toLocaleString('id-ID')}</td>
                        <td style="color: ${(record.profit || 0) >= 0 ? '#10b981' : '#ef4444'}; font-weight: bold;">
                            Rp ${(record.profit || 0).toLocaleString('id-ID')}
                        </td>
                        <td style="font-weight: 600;">${(record.profit_margin || 0).toFixed(1)}%</td>
                        <td>
                            <button class="btn btn-danger btn-small" onclick="event.stopPropagation(); deleteRecord('${record.id}')">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>'''

content = re.sub(
    r'<tr onclick="toggleDetails\(\'\$\{record\.id\}\'\)" style="cursor: pointer;">.*?</tr>',
    row_update,
    content,
    flags=re.DOTALL,
    count=1
)

# Write updated content
with open('templates/modules/harvest_database.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Enhanced Harvest Database HTML with cost tracking!")
print("✅ Added: Cost input form, profit calculation, enhanced table")
