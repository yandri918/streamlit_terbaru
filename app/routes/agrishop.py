"""API routes for AgriShop marketplace."""
from flask import Blueprint, request, jsonify, render_template
from app.services.agrishop_service import AgriShopService

agrishop_bp = Blueprint('agrishop', __name__)
agrishop_service = AgriShopService()


# ========== FRONTEND ROUTES ==========

@agrishop_bp.route('/modules/agrishop')
def agrishop_page():
    """Render AgriShop marketplace page."""
    return render_template('modules/agrishop.html')


# ========== PRODUCT ENDPOINTS ==========

@agrishop_bp.route('/api/agrishop/products', methods=['GET'])
def get_products():
    """Get all products with optional filters."""
    try:
        # Get query parameters
        commodity = request.args.get('commodity')
        quality_grade = request.args.get('quality_grade')
        status = request.args.get('status', 'available')
        is_preorder = request.args.get('is_preorder')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Location-based filtering
        user_lat = request.args.get('lat', type=float)
        user_lon = request.args.get('lon', type=float)
        max_distance = request.args.get('max_distance_km', type=float)
        
        # Convert is_preorder to boolean
        if is_preorder is not None:
            is_preorder = is_preorder.lower() == 'true'
        
        # Get products with distance if location provided
        if user_lat and user_lon:
            products = agrishop_service.get_products_with_distance(
                user_lat, user_lon, max_distance,
                commodity=commodity,
                quality_grade=quality_grade,
                status=status,
                is_preorder=is_preorder,
                min_price=min_price,
                max_price=max_price
            )
        else:
            products = agrishop_service.db.get_products(
                commodity=commodity,
                quality_grade=quality_grade,
                status=status,
                is_preorder=is_preorder,
                min_price=min_price,
                max_price=max_price
            )
        
        # Add quality badges to each product
        for product in products:
            product['badges'] = agrishop_service.get_quality_badges(product)
        
        return jsonify({
            'success': True,
            'count': len(products),
            'data': products
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@agrishop_bp.route('/api/agrishop/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get product by ID and increment view count."""
    try:
        product = agrishop_service.db.get_product_by_id(product_id)
        
        if not product:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        
        # Increment view count
        agrishop_service.db.increment_views(product_id)
        product['views'] = product.get('views', 0) + 1
        
        # Add badges
        product['badges'] = agrishop_service.get_quality_badges(product)
        
        # Get pre-orders for this product
        preorders = agrishop_service.db.get_preorders(product_id)
        product['preorder_count'] = len(preorders)
        
        return jsonify({'success': True, 'data': product})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@agrishop_bp.route('/api/agrishop/products', methods=['POST'])
def add_product():
    """Add a new product."""
    try:
        data = request.get_json()
        
        # Validate data
        validation = agrishop_service.validate_product_data(data)
        if not validation['valid']:
            return jsonify({
                'success': False,
                'errors': validation['errors']
            }), 400
        
        # Add product
        product = agrishop_service.db.add_product(
            seller_name=data['seller_name'],
            seller_phone=data['seller_phone'],
            commodity=data['commodity'],
            quantity_kg=float(data['quantity_kg']),
            price_per_kg=float(data['price_per_kg']),
            quality_grade=data['quality_grade'],
            harvest_date=data.get('harvest_date', ''),
            latitude=float(data.get('latitude', 0)),
            longitude=float(data.get('longitude', 0)),
            address=data.get('address', ''),
            photo_url=data.get('photo_url', ''),
            description=data.get('description', ''),
            is_preorder=data.get('is_preorder', False)
        )
        
        return jsonify({'success': True, 'data': product}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@agrishop_bp.route('/api/agrishop/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product."""
    try:
        data = request.get_json()
        
        success = agrishop_service.db.update_product(product_id, data)
        
        if success:
            product = agrishop_service.db.get_product_by_id(product_id)
            return jsonify({'success': True, 'data': product})
        else:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@agrishop_bp.route('/api/agrishop/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete product."""
    try:
        success = agrishop_service.db.delete_product(product_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Product deleted'})
        else:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@agrishop_bp.route('/api/agrishop/products/<product_id>/interest', methods=['POST'])
def mark_interest(product_id):
    """Mark interest in a product."""
    try:
        success = agrishop_service.db.increment_interests(product_id)
        
        if success:
            product = agrishop_service.db.get_product_by_id(product_id)
            return jsonify({
                'success': True,
                'interests': product.get('interests', 0)
            })
        else:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== PRICE RECOMMENDATION ==========

@agrishop_bp.route('/api/agrishop/price-recommendation', methods=['GET'])
def get_price_recommendation():
    """Get smart price recommendation."""
    try:
        commodity = request.args.get('commodity')
        quality_grade = request.args.get('quality_grade', 'B')
        lat = request.args.get('lat', type=float, default=0)
        lon = request.args.get('lon', type=float, default=0)
        
        if not commodity:
            return jsonify({'success': False, 'error': 'Commodity is required'}), 400
        
        recommendation = agrishop_service.get_price_recommendation(
            commodity, quality_grade, lat, lon
        )
        
        return jsonify(recommendation)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== PRE-ORDER ENDPOINTS ==========

@agrishop_bp.route('/api/agrishop/preorders', methods=['POST'])
def add_preorder():
    """Add a pre-order."""
    try:
        data = request.get_json()
        
        required = ['product_id', 'buyer_name', 'buyer_phone', 'quantity_kg']
        if not all(field in data for field in required):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Calculate total
        calculation = agrishop_service.calculate_preorder_total(
            data['product_id'],
            float(data['quantity_kg'])
        )
        
        if not calculation['success']:
            return jsonify(calculation), 400
        
        # Add pre-order
        preorder = agrishop_service.db.add_preorder(
            product_id=data['product_id'],
            buyer_name=data['buyer_name'],
            buyer_phone=data['buyer_phone'],
            quantity_kg=float(data['quantity_kg']),
            notes=data.get('notes', '')
        )
        
        # Add calculation to response
        preorder['calculation'] = calculation
        
        return jsonify({'success': True, 'data': preorder}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@agrishop_bp.route('/api/agrishop/preorders/<preorder_id>/status', methods=['PUT'])
def update_preorder_status(preorder_id):
    """Update pre-order status."""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if status not in ['pending', 'confirmed', 'completed', 'cancelled']:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        
        success = agrishop_service.db.update_preorder_status(preorder_id, status)
        
        if success:
            return jsonify({'success': True, 'message': 'Status updated'})
        else:
            return jsonify({'success': False, 'error': 'Pre-order not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== SELLER DASHBOARD ==========

@agrishop_bp.route('/api/agrishop/my-products', methods=['GET'])
def get_my_products():
    """Get products for a specific seller."""
    try:
        seller_phone = request.args.get('seller_phone')
        
        if not seller_phone:
            return jsonify({'success': False, 'error': 'seller_phone is required'}), 400
        
        all_products = agrishop_service.db.get_products()
        my_products = [p for p in all_products if p.get('seller_phone') == seller_phone]
        
        # Get statistics
        stats = agrishop_service.get_seller_statistics(seller_phone)
        
        return jsonify({
            'success': True,
            'count': len(my_products),
            'data': my_products,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== STATISTICS ==========

@agrishop_bp.route('/api/agrishop/statistics', methods=['GET'])
def get_statistics():
    """Get marketplace statistics."""
    try:
        stats = agrishop_service.db.get_statistics()
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
