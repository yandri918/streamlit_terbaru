"""Authentication routes for user management."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from app import db, limiter
from app.models.user import User
from app.models.user_activity import UserActivity

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields',
                'required': required_fields
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'success': False,
                'error': 'Username already exists'
            }), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'error': 'Email already exists'
            }), 409
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            full_name=data.get('full_name'),
            phone=data.get('phone'),
            location=data.get('location'),
            farm_size=data.get('farm_size')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Registration failed',
            'message': str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per hour")
def login():
    """Login user and return JWT tokens."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'Username and password are required'
            }), 400
        
        # Find user
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'error': 'Invalid username or password'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Account is deactivated'
            }), 403
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Login failed',
            'message': str(e)
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token."""
    try:
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'success': True,
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Token refresh failed',
            'message': str(e)
        }), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get user information',
            'message': str(e)
        }), 500


@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """Update current user information."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['full_name', 'phone', 'location', 'farm_size']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to update user',
            'message': str(e)
        }), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        data = request.get_json()
        
        if not data.get('old_password') or not data.get('new_password'):
            return jsonify({
                'success': False,
                'error': 'Old password and new password are required'
            }), 400
        
        # Verify old password
        if not user.check_password(data['old_password']):
            return jsonify({
                'success': False,
                'error': 'Invalid old password'
            }), 401
        
        # Set new password
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to change password',
            'message': str(e)
        }), 500


# ========== STREAMLIT INTEGRATION ENDPOINTS ==========

@auth_bp.route('/simple-login', methods=['POST'])
def simple_login():
    """
    Simple login for Streamlit (without JWT).
    Returns user data directly.
    """
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Username dan password harus diisi'
            }), 400
        
        username = data['username'].strip().lower()
        user = User.query.filter_by(username=username).first()
        
        if not user:
            UserActivity.log_activity(
                username=username,
                action='LOGIN_FAILED',
                details='User tidak ditemukan',
                ip_address=request.remote_addr
            )
            return jsonify({
                'success': False,
                'message': 'Username tidak ditemukan'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'message': 'Akun tidak aktif'
            }), 401
        
        if not user.check_password(data['password']):
            UserActivity.log_activity(
                username=username,
                action='LOGIN_FAILED',
                details='Password salah',
                user_id=user.id,
                ip_address=request.remote_addr
            )
            return jsonify({
                'success': False,
                'message': 'Password salah'
            }), 401
        
        # Log successful login
        UserActivity.log_activity(
            username=username,
            action='LOGIN',
            details=f'Login sebagai {user.role}',
            user_id=user.id,
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'success': True,
            'message': f'Selamat datang, {user.full_name or user.username}!',
            'user': {
                'id': user.id,
                'username': user.username,
                'name': user.full_name or user.username,
                'email': user.email,
                'role': user.role
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@auth_bp.route('/simple-register', methods=['POST'])
def simple_register():
    """
    Simple register for Streamlit (without JWT).
    """
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        email = data.get('email', '').strip() or f"{username}@agrisensa.com"
        
        if not username or not password or not name:
            return jsonify({
                'success': False,
                'message': 'Username, password, dan nama harus diisi'
            }), 400
        
        if len(username) < 3:
            return jsonify({
                'success': False,
                'message': 'Username minimal 3 karakter'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'success': False,
                'message': 'Password minimal 6 karakter'
            }), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'message': 'Username sudah digunakan'
            }), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'message': 'Email sudah digunakan'
            }), 400
        
        user = User(
            username=username,
            email=email,
            full_name=name,
            role='user'
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        UserActivity.log_activity(
            username=username,
            action='REGISTER',
            details='User baru mendaftar',
            user_id=user.id,
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'success': True,
            'message': f'Selamat datang, {name}! Akun berhasil dibuat.',
            'user': {
                'id': user.id,
                'username': user.username,
                'name': user.full_name,
                'email': user.email,
                'role': user.role
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@auth_bp.route('/log-activity', methods=['POST'])
def log_activity():
    """Log user activity."""
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        action = data.get('action', '').strip()
        details = data.get('details', '')
        
        if not username or not action:
            return jsonify({
                'success': False,
                'message': 'Username dan action diperlukan'
            }), 400
        
        UserActivity.log_activity(
            username=username,
            action=action,
            details=details,
            ip_address=request.remote_addr
        )
        
        return jsonify({'success': True, 'message': 'Activity logged'})
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@auth_bp.route('/activities', methods=['GET'])
def get_activities():
    """Get user activities for Super Admin."""
    try:
        limit = request.args.get('limit', 100, type=int)
        username = request.args.get('username', '').strip()
        
        if username:
            activities = UserActivity.get_user_activities(username, limit)
        else:
            activities = UserActivity.get_recent_activities(limit)
        
        return jsonify({
            'success': True,
            'activities': [a.to_dict() for a in activities],
            'total': len(activities)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@auth_bp.route('/users-list', methods=['GET'])
def get_users_list():
    """Get all users for Super Admin."""
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'users': [u.to_dict() for u in users],
            'total': len(users)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
