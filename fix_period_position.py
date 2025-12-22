"""Fix period selector position - move it before date input"""

# Read the file
with open('templates/modules/analisis_tren_harga.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the wrongly placed period selector (after button)
content = content.replace("""
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
                        </div>""", "")

# Insert it in the correct position (after commodity select, before date input)
old_section = """                        </div>

                        <div>
                            <label for="target-date" class="block text-sm font-medium text-gray-700 mb-1">Target Tanggal
                                Prediksi</label>"""

new_section = """                        </div>

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

                        <div>
                            <label for="target-date" class="block text-sm font-medium text-gray-700 mb-1">Target Tanggal
                                Prediksi</label>"""

content = content.replace(old_section, new_section)

# Write back
with open('templates/modules/analisis_tren_harga.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Period selector position fixed!")
