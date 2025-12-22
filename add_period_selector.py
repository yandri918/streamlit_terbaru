"""Safely add period selector to analisis_tren_harga.html"""

# Read the original file
with open('templates/modules/analisis_tren_harga.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line after commodity select (line 108: </div>)
# Insert period selector after it
insert_position = 108  # After </div> of commodity select

period_selector = """
                        <div>
                            <label for="period-select" class="block text-sm font-medium text-gray-700 mb-1">Periode Visualisasi</label>
                            <select id="period-select"
                                class="w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border">
                                <option value="7">7 Hari Terakhir</option>
                                <option value="30" selected>30 Hari Terakhir</option>
                                <option value="90">90 Hari (3 Bulan)</option>
                                <option value="180">180 Hari (6 Bulan)</option>
                                <option value="365">365 Hari (1 Tahun)</option>
                            </select>
                            <p class="text-xs text-gray-500 mt-1">Pilih periode untuk melihat tren historis</p>
                        </div>
"""

# Insert the period selector
lines.insert(insert_position, period_selector)

# Write back
with open('templates/modules/analisis_tren_harga.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Period selector added successfully!")
print(f"   Inserted at line {insert_position}")
