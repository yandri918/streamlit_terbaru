"""Add harvest sequence number field to harvest database."""

with open('templates/modules/harvest_database.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add harvest sequence field after harvest date
sequence_field = '''
                    <div class="form-group">
                        <label>Panen Ke-</label>
                        <input type="number" id="harvest-sequence" min="1" value="1" required>
                        <small style="color: #718096; display: block; margin-top: 5px;">
                            Untuk tanaman yang dipanen bertahap (cabe, tomat, dll)
                        </small>
                    </div>
                </div>

                <div class="form-row">'''

content = content.replace(
    '''                    <div class="form-group">
                        <label>Tanggal Panen *</label>
                        <input type="date" id="harvest-date" required>
                    </div>
                </div>

                <div class="form-group">''',
    '''                    <div class="form-group">
                        <label>Tanggal Panen *</label>
                        <input type="date" id="harvest-date" required>
                    </div>
                    ''' + sequence_field + '''<div class="form-group">'''
)

# 2. Update submitRecord to include harvest_sequence
content = content.replace(
    "harvest_date: document.getElementById('harvest-date').value,",
    "harvest_date: document.getElementById('harvest-date').value,\n                harvest_sequence: parseInt(document.getElementById('harvest-sequence').value) || 1,"
)

# 3. Update table to show sequence
content = content.replace(
    '<td>${record.harvest_date}</td>',
    '<td>${record.harvest_date} <span style="background: #3b82f6; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; margin-left: 5px;">#${record.harvest_sequence || 1}</span></td>'
)

# Write updated content
with open('templates/modules/harvest_database.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added harvest sequence field!")
print("✅ Petani bisa track panen ke-1, ke-2, ke-3, dst")
