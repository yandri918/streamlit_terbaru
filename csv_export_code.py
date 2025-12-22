"""Add CSV export functionality to harvest database."""
import csv
import io
from flask import make_response

# This will be added to harvest_routes.py

export_route = '''

@harvest_bp.route('/api/harvest/export/csv', methods=['GET'])
def export_to_csv():
    """Export harvest records to CSV."""
    try:
        farmer_phone = request.args.get('farmer_phone')
        
        # Get records
        records = harvest_service.db.get_records(farmer_phone=farmer_phone)
        
        if not records:
            return jsonify({'success': False, 'error': 'No records found'}), 404
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Tanggal Panen',
            'Panen Ke-',
            'Nama Petani',
            'No. HP',
            'Komoditas',
            'Lokasi',
            'Cuaca',
            'Total Quantity (kg)',
            'Total Nilai (Rp)',
            'Biaya Bibit (Rp)',
            'Biaya Pupuk (Rp)',
            'Biaya Pestisida (Rp)',
            'Biaya Tenaga Kerja (Rp)',
            'Biaya Lainnya (Rp)',
            'Total Biaya (Rp)',
            'Profit (Rp)',
            'Profit Margin (%)',
            'ROI (%)',
            'Biaya per kg (Rp)',
            'Harga per kg (Rp)',
            'Catatan'
        ])
        
        # Write data rows
        for record in records:
            costs = record.get('costs', {})
            writer.writerow([
                record.get('harvest_date', ''),
                record.get('harvest_sequence', 1),
                record.get('farmer_name', ''),
                record.get('farmer_phone', ''),
                record.get('commodity', ''),
                record.get('location', ''),
                record.get('weather', ''),
                record.get('total_quantity', 0),
                record.get('total_value', 0),
                costs.get('bibit', 0),
                costs.get('pupuk', 0),
                costs.get('pestisida', 0),
                costs.get('tenaga_kerja', 0),
                costs.get('lainnya', 0),
                record.get('total_cost', 0),
                record.get('profit', 0),
                record.get('profit_margin', 0),
                record.get('roi', 0),
                record.get('cost_per_kg', 0),
                record.get('revenue_per_kg', 0),
                record.get('notes', '')
            ])
        
        # Create response
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=harvest_data_{farmer_phone or "all"}.csv'
        
        return response
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
'''

print("CSV export route code generated!")
print("This will be added to harvest_routes.py")
