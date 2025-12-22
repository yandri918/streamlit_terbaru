"""API routes for Harvest Storage."""
from flask import Blueprint, request, jsonify, render_template, make_response
from app.services.harvest_service import HarvestService
import csv
import io

harvest_bp = Blueprint('harvest', __name__)
harvest_service = HarvestService()


# ========== FRONTEND ROUTES ==========

@harvest_bp.route('/modules/harvest-database')
def harvest_database_page():
    """Render harvest database page."""
    return render_template('modules/harvest_database.html')


# ========== HARVEST RECORD ENDPOINTS ==========

@harvest_bp.route('/api/harvest/records', methods=['GET'])
def get_records():
    """Get all harvest records with optional filters."""
    try:
        farmer_phone = request.args.get('farmer_phone')
        commodity = request.args.get('commodity')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        records = harvest_service.db.get_records(
            farmer_phone=farmer_phone,
            commodity=commodity,
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify({
            'success': True,
            'count': len(records),
            'data': records
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@harvest_bp.route('/api/harvest/records/<record_id>', methods=['GET'])
def get_record(record_id):
    """Get harvest record by ID."""
    try:
        record = harvest_service.db.get_record_by_id(record_id)
        
        if not record:
            return jsonify({'success': False, 'error': 'Record not found'}), 404
        
        return jsonify({'success': True, 'data': record})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@harvest_bp.route('/api/harvest/records', methods=['POST'])
def add_record():
    """Add a new harvest record."""
    try:
        data = request.get_json()
        
        # Validate data
        validation = harvest_service.validate_record_data(data)
        if not validation['valid']:
            return jsonify({
                'success': False,
                'errors': validation['errors']
            }), 400
        
        # Prepare criteria with calculated totals
        criteria = harvest_service.prepare_criteria(data['criteria'])
        
        # Add record with costs and additional fields
        record = harvest_service.db.add_record(
            farmer_name=data['farmer_name'],
            farmer_phone=data['farmer_phone'],
            commodity=data['commodity'],
            location=data['location'],
            harvest_date=data['harvest_date'],
            criteria=criteria,
            costs=data.get('costs', {}),
            notes=data.get('notes', ''),
            weather=data.get('weather', ''),
            harvest_sequence=data.get('harvest_sequence', 1)
        )
        
        return jsonify({'success': True, 'data': record}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@harvest_bp.route('/api/harvest/records/<record_id>', methods=['PUT'])
def update_record(record_id):
    """Update harvest record."""
    try:
        data = request.get_json()
        
        # Prepare criteria if provided
        if 'criteria' in data:
            data['criteria'] = harvest_service.prepare_criteria(data['criteria'])
        
        success = harvest_service.db.update_record(record_id, data)
        
        if success:
            record = harvest_service.db.get_record_by_id(record_id)
            return jsonify({'success': True, 'data': record})
        else:
            return jsonify({'success': False, 'error': 'Record not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@harvest_bp.route('/api/harvest/records/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete harvest record."""
    try:
        success = harvest_service.db.delete_record(record_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Record deleted'})
        else:
            return jsonify({'success': False, 'error': 'Record not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== STATISTICS & ANALYTICS ==========

@harvest_bp.route('/api/harvest/statistics', methods=['GET'])
def get_statistics():
    """Get harvest statistics."""
    try:
        farmer_phone = request.args.get('farmer_phone')
        stats = harvest_service.db.get_statistics(farmer_phone=farmer_phone)
        
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@harvest_bp.route('/api/harvest/chart-data', methods=['GET'])
def get_chart_data():
    """Get data formatted for charts."""
    try:
        farmer_phone = request.args.get('farmer_phone')
        chart_data = harvest_service.db.get_chart_data(farmer_phone=farmer_phone)
        
        return jsonify({'success': True, 'data': chart_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@harvest_bp.route('/api/harvest/my-summary', methods=['GET'])
def get_my_summary():
    """Get farmer's summary."""
    try:
        farmer_phone = request.args.get('farmer_phone')
        
        if not farmer_phone:
            return jsonify({'success': False, 'error': 'farmer_phone is required'}), 400
        
        summary = harvest_service.get_farmer_summary(farmer_phone)
        
        return jsonify({'success': True, 'data': summary})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== EXPORT & REPORTING ==========

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
        response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'  # UTF-8 with BOM for Excel
        response.headers['Content-Disposition'] = f'attachment; filename=harvest_data_{farmer_phone or "all"}.csv'
        
        return response
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
