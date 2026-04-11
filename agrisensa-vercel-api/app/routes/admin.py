"""Admin API routes for managing commodities, prices, and users."""
from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from functools import wraps
from datetime import datetime

from app import db
from app.models import User, Commodity, ManualPrice, AdminAuditLog

admin_bp = Blueprint('admin', __name__)


# ========== DECORATORS ==========
def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({
                'success': False,
                'error': 'Admin access required'
            }), 403
        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function


def log_admin_action(action, table_name=None, record_id=None, old_values=None, new_values=None, notes=None):
    """Helper to log admin actions."""
    user = getattr(g, 'current_user', None)
    AdminAuditLog.log_action(
        user_id=user.id if user else None,
        username=user.username if user else 'system',
        action=action,
        table_name=table_name,
        record_id=record_id,
        old_values=old_values,
        new_values=new_values,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent', '')[:255],
        endpoint=request.endpoint,
        notes=notes
    )


# ========== AUTH ENDPOINTS ==========
@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """Admin login endpoint."""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    if user.role != 'admin':
        return jsonify({'success': False, 'error': 'Admin access required'}), 403
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    # Log the login
    AdminAuditLog.log_action(
        user_id=user.id,
        username=user.username,
        action='LOGIN',
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent', '')[:255],
        notes='Admin login successful'
    )
    
    return jsonify({
        'success': True,
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    })


@admin_bp.route('/profile', methods=['GET'])
@admin_required
def get_profile():
    """Get current admin profile."""
    user = g.current_user
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
    })


# ========== DASHBOARD STATS ==========
@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_dashboard_stats():
    """Get dashboard statistics."""
    stats = {
        'total_commodities': Commodity.query.count(),
        'active_commodities': Commodity.query.filter_by(is_active=True).count(),
        'total_manual_prices': ManualPrice.query.count(),
        'unverified_prices': ManualPrice.query.filter_by(is_verified=False).count(),
        'total_users': User.query.count(),
        'admin_users': User.query.filter_by(role='admin').count(),
        'recent_activity': AdminAuditLog.get_activity_summary(days=7)
    }
    
    return jsonify({
        'success': True,
        'stats': stats
    })


# ========== COMMODITIES CRUD ==========
@admin_bp.route('/commodities', methods=['GET'])
@admin_required
def list_commodities():
    """List all commodities with optional filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')
    search = request.args.get('search')
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    
    query = Commodity.query
    
    if active_only:
        query = query.filter(Commodity.is_active == True)
    if category:
        query = query.filter(Commodity.category == category)
    if search:
        query = query.filter(
            db.or_(
                Commodity.name.ilike(f'%{search}%'),
                Commodity.name_local.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(Commodity.name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'commodities': [c.to_dict() for c in pagination.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })


@admin_bp.route('/commodities/<int:id>', methods=['GET'])
@admin_required
def get_commodity(id):
    """Get a single commodity by ID."""
    commodity = Commodity.query.get_or_404(id)
    return jsonify({
        'success': True,
        'commodity': commodity.to_dict()
    })


@admin_bp.route('/commodities', methods=['POST'])
@admin_required
def create_commodity():
    """Create a new commodity."""
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('category'):
        return jsonify({
            'success': False,
            'error': 'Name and category are required'
        }), 400
    
    # Check for duplicate name
    if Commodity.query.filter_by(name=data['name']).first():
        return jsonify({
            'success': False,
            'error': 'Commodity with this name already exists'
        }), 400
    
    commodity = Commodity(
        name=data['name'],
        name_local=data.get('name_local'),
        category=data['category'],
        subcategory=data.get('subcategory'),
        unit=data.get('unit', 'kg'),
        optimal_ph_min=data.get('optimal_ph_min'),
        optimal_ph_max=data.get('optimal_ph_max'),
        optimal_temp_min=data.get('optimal_temp_min'),
        optimal_temp_max=data.get('optimal_temp_max'),
        optimal_altitude_min=data.get('optimal_altitude_min'),
        optimal_altitude_max=data.get('optimal_altitude_max'),
        water_need=data.get('water_need'),
        days_to_harvest_min=data.get('days_to_harvest_min'),
        days_to_harvest_max=data.get('days_to_harvest_max'),
        yield_per_hectare_min=data.get('yield_per_hectare_min'),
        yield_per_hectare_max=data.get('yield_per_hectare_max'),
        price_reference=data.get('price_reference'),
        price_source=data.get('price_source', 'manual'),
        description=data.get('description'),
        cultivation_guide=data.get('cultivation_guide'),
        is_active=data.get('is_active', True),
        is_featured=data.get('is_featured', False),
        image_url=data.get('image_url'),
        created_by=g.current_user.id
    )
    
    db.session.add(commodity)
    db.session.commit()
    
    log_admin_action('CREATE', 'commodities', commodity.id, new_values=commodity.to_dict())
    
    return jsonify({
        'success': True,
        'message': 'Commodity created successfully',
        'commodity': commodity.to_dict()
    }), 201


@admin_bp.route('/commodities/<int:id>', methods=['PUT'])
@admin_required
def update_commodity(id):
    """Update an existing commodity."""
    commodity = Commodity.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    old_values = commodity.to_dict()
    
    # Update fields
    for field in ['name', 'name_local', 'category', 'subcategory', 'unit',
                  'optimal_ph_min', 'optimal_ph_max', 'optimal_temp_min', 'optimal_temp_max',
                  'optimal_altitude_min', 'optimal_altitude_max', 'water_need',
                  'days_to_harvest_min', 'days_to_harvest_max',
                  'yield_per_hectare_min', 'yield_per_hectare_max',
                  'price_reference', 'price_source', 'description', 'cultivation_guide',
                  'is_active', 'is_featured', 'image_url']:
        if field in data:
            setattr(commodity, field, data[field])
    
    commodity.updated_by = g.current_user.id
    db.session.commit()
    
    log_admin_action('UPDATE', 'commodities', commodity.id, 
                     old_values=old_values, new_values=commodity.to_dict())
    
    return jsonify({
        'success': True,
        'message': 'Commodity updated successfully',
        'commodity': commodity.to_dict()
    })


@admin_bp.route('/commodities/<int:id>', methods=['DELETE'])
@admin_required
def delete_commodity(id):
    """Soft delete a commodity (set is_active=False)."""
    commodity = Commodity.query.get_or_404(id)
    old_values = commodity.to_dict()
    
    commodity.is_active = False
    commodity.updated_by = g.current_user.id
    db.session.commit()
    
    log_admin_action('DELETE', 'commodities', commodity.id, old_values=old_values,
                     notes='Soft delete - commodity deactivated')
    
    return jsonify({
        'success': True,
        'message': 'Commodity deactivated successfully'
    })


@admin_bp.route('/commodities/bulk', methods=['POST'])
@admin_required
def bulk_import_commodities():
    """Bulk import commodities from JSON array."""
    data = request.get_json()
    
    if not data or not isinstance(data, list):
        return jsonify({
            'success': False,
            'error': 'Expected JSON array of commodities'
        }), 400
    
    created = 0
    updated = 0
    errors = []
    
    for item in data:
        try:
            existing = Commodity.query.filter_by(name=item.get('name')).first()
            if existing:
                # Update existing
                for field in ['category', 'subcategory', 'unit', 'price_reference']:
                    if field in item:
                        setattr(existing, field, item[field])
                updated += 1
            else:
                # Create new
                commodity = Commodity(
                    name=item['name'],
                    category=item.get('category', 'Lainnya'),
                    unit=item.get('unit', 'kg'),
                    price_reference=item.get('price_reference'),
                    created_by=g.current_user.id
                )
                db.session.add(commodity)
                created += 1
        except Exception as e:
            errors.append({'item': item.get('name'), 'error': str(e)})
    
    db.session.commit()
    
    log_admin_action('BULK_IMPORT', 'commodities', 
                     notes=f'Created: {created}, Updated: {updated}, Errors: {len(errors)}')
    
    return jsonify({
        'success': True,
        'message': f'Bulk import completed',
        'result': {
            'created': created,
            'updated': updated,
            'errors': errors
        }
    })


# ========== MANUAL PRICES ==========
@admin_bp.route('/prices', methods=['GET'])
@admin_required
def list_manual_prices():
    """List all manual prices."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    commodity_id = request.args.get('commodity_id', type=int)
    province_id = request.args.get('province_id', type=int)
    
    query = ManualPrice.query
    
    if commodity_id:
        query = query.filter(ManualPrice.commodity_id == commodity_id)
    if province_id:
        query = query.filter(ManualPrice.province_id == province_id)
    
    pagination = query.order_by(ManualPrice.price_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'prices': [p.to_dict() for p in pagination.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })


@admin_bp.route('/prices', methods=['POST'])
@admin_required
def create_manual_price():
    """Create a new manual price entry."""
    data = request.get_json()
    
    if not data or not data.get('commodity_id') or not data.get('price'):
        return jsonify({
            'success': False,
            'error': 'commodity_id and price are required'
        }), 400
    
    price = ManualPrice(
        commodity_id=data['commodity_id'],
        province_id=data.get('province_id'),
        province_name=data.get('province_name'),
        city_name=data.get('city_name'),
        price=data['price'],
        price_type=data.get('price_type', 'retail'),
        unit=data.get('unit', 'kg'),
        price_date=datetime.strptime(data['price_date'], '%Y-%m-%d').date() if data.get('price_date') else None,
        source=data.get('source', 'manual'),
        notes=data.get('notes'),
        reported_by=g.current_user.id
    )
    
    db.session.add(price)
    db.session.commit()
    
    log_admin_action('CREATE', 'manual_prices', price.id, new_values=price.to_dict())
    
    return jsonify({
        'success': True,
        'message': 'Price created successfully',
        'price': price.to_dict()
    }), 201


@admin_bp.route('/prices/<int:id>', methods=['DELETE'])
@admin_required
def delete_manual_price(id):
    """Delete a manual price entry."""
    price = ManualPrice.query.get_or_404(id)
    old_values = price.to_dict()
    
    db.session.delete(price)
    db.session.commit()
    
    log_admin_action('DELETE', 'manual_prices', id, old_values=old_values)
    
    return jsonify({
        'success': True,
        'message': 'Price deleted successfully'
    })


# ========== AUDIT LOG ==========
@admin_bp.route('/audit-log', methods=['GET'])
@admin_required
def get_audit_log():
    """Get audit log entries."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    action = request.args.get('action')
    table_name = request.args.get('table')
    user_id = request.args.get('user_id', type=int)
    
    query = AdminAuditLog.query
    
    if action:
        query = query.filter(AdminAuditLog.action == action)
    if table_name:
        query = query.filter(AdminAuditLog.table_name == table_name)
    if user_id:
        query = query.filter(AdminAuditLog.user_id == user_id)
    
    pagination = query.order_by(AdminAuditLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'logs': [l.to_dict() for l in pagination.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })


# ========== CATEGORIES ==========
@admin_bp.route('/categories', methods=['GET'])
@admin_required
def get_categories():
    """Get list of commodity categories."""
    categories = db.session.query(Commodity.category).distinct().all()
    return jsonify({
        'success': True,
        'categories': [c[0] for c in categories if c[0]]
    })
