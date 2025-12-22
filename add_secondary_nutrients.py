import re

# Read the file
with open('templates/modules/kalkulator_pupuk_holistik.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the location to insert (after "html += '</div>';")
# We'll insert after the summary grid closing div
secondary_nutrients_section = '''
            // Secondary Macro Nutrients Section
            html += `
                <h3 style="margin-top: 30px; margin-bottom: 15px; color: var(--primary-dark);">🧪 Kebutuhan Hara Makro Sekunder</h3>
                <div class="info-box" style="background: #f0f9ff; border-left-color: var(--secondary);">
                    <div class="info-box-title" style="color: var(--secondary);">📊 Kalsium (Ca), Magnesium (Mg), Sulfur (S)</div>
                    <div class="info-box-content" style="color: #1e40af;">
                        <div style="margin-top: 12px;">
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 10px;">
                                <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #dbeafe;">
                                    <div style="font-weight: 700; color: var(--secondary); margin-bottom: 8px;">🔹 Kalsium (Ca)</div>
                                    <div style="font-size: 0.9rem;">
                                        <strong>Fungsi:</strong> Pembentukan dinding sel, pertumbuhan akar<br>
                                        <strong>Sumber:</strong> Dolomit, Kapur Pertanian, Gypsum<br>
                                        <strong>Dosis:</strong> 200-500 kg/ha
                                    </div>
                                </div>
                                <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #dbeafe;">
                                    <div style="font-weight: 700; color: var(--secondary); margin-bottom: 8px;">🔹 Magnesium (Mg)</div>
                                    <div style="font-size: 0.9rem;">
                                        <strong>Fungsi:</strong> Komponen klorofil, aktivasi enzim<br>
                                        <strong>Sumber:</strong> Dolomit, Kieserit, MgSO₄<br>
                                        <strong>Dosis:</strong> 50-150 kg/ha
                                    </div>
                                </div>
                                <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #dbeafe;">
                                    <div style="font-weight: 700; color: var(--secondary); margin-bottom: 8px;">🔹 Sulfur (S)</div>
                                    <div style="font-size: 0.9rem;">
                                        <strong>Fungsi:</strong> Sintesis protein, pembentukan klorofil<br>
                                        <strong>Sumber:</strong> ZA, Gypsum, Elemental S<br>
                                        <strong>Dosis:</strong> 20-40 kg/ha
                                    </div>
                                </div>
                            </div>
                            <div style="margin-top: 15px; padding: 12px; background: #fef3c7; border-radius: 6px; border-left: 3px solid var(--accent);">
                                <strong style="color: #92400e;">💡 Catatan:</strong>
                                <span style="color: #78350f; font-size: 0.9rem;">
                                    Hara sekunder sering diabaikan namun sangat penting untuk hasil optimal. 
                                    Aplikasikan bersamaan dengan pengapuran atau sebagai pupuk dasar.
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            `;

'''

# Find the pattern to insert after
pattern = r"(html \+= '</div>';[\r\n]+[\r\n]+            // Notes)"

# Replace with the pattern + our new section
replacement = r"html += '</div>';\n\n" + secondary_nutrients_section + "\n            // Notes"

new_content = re.sub(pattern, replacement, content)

# Write back
with open('templates/modules/kalkulator_pupuk_holistik.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Secondary nutrients section added successfully!")
