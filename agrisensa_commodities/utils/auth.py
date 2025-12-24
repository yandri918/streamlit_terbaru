"""
Authentication utility for AgriSensa Streamlit
Database-backed via Vercel API with session fallback and local persistence
"""

import streamlit as st
import requests
from datetime import datetime
import json
import os

# ========== API CONFIGURATION ==========
API_BASE_URL = "https://agriisensa-api2.vercel.app"

# ========== LOCAL DATA STORAGE ==========
# Point to central agrisensa_tech/data for shared users
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# commodities/utils -> commodities -> root -> agrisensa_tech -> data
REPO_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
DATA_DIR = os.path.join(REPO_ROOT, "agrisensa_tech", "data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
SESSION_FILE = os.path.join(DATA_DIR, "session.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# ========== DEFAULT USERS (Fallback) ==========
DEFAULT_USERS = {
    'yandri': {
        'password': 'yandri2025',
        'role': 'superadmin',
        'name': 'Yandri - Owner',
        'email': 'yandri@agrisensa.com'
    },
    'admin': {
        'password': 'admin123',
        'role': 'admin',
        'name': 'Administrator',
        'email': 'admin@agrisensa.com'
    },
    'demo': {
        'password': 'demo123',
        'role': 'user',
        'name': 'Demo User',
        'email': 'demo@agrisensa.com'
    },
    'petani': {
        'password': 'petani123',
        'role': 'user',
        'name': 'Petani Indonesia',
        'email': 'petani@agrisensa.com'
    }
}


def load_local_users():
    """Load users from local JSON file."""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}
    return {}


def save_local_users(users):
    """Save users to local JSON file."""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    except Exception as e:
        print(f"Error saving users: {e}")


def load_session():
    """Load persistent session from local file."""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None


def save_session(username):
    """Save persistent session to local file."""
    try:
        data = {
            'username': username,
            'timestamp': datetime.now().isoformat()
        }
        with open(SESSION_FILE, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving session: {e}")


def clear_session():
    """Clear persistent session."""
    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
        except:
            pass


def api_request(endpoint: str, method: str = 'GET', data: dict = None) -> dict:
    """Make API request with error handling."""
    try:
        url = f"{API_BASE_URL}/api/auth/{endpoint}"
        if method == 'GET':
            response = requests.get(url, params=data, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        return {'success': False, 'message': f'API Error: {str(e)}', 'api_error': True}


def get_users():
    """Get users from session state or local storage."""
    if 'registered_users' not in st.session_state:
        # Combine DEFAULT_USERS with LOCAL_USERS
        local_users = load_local_users()
        all_users = DEFAULT_USERS.copy()
        all_users.update(local_users)
        st.session_state.registered_users = all_users
    return st.session_state.registered_users


def get_activity_log():
    """Get user activity log from API."""
    if 'user_activity_log' not in st.session_state:
        st.session_state.user_activity_log = []
    
    # Try to get from API
    result = api_request('activities')
    if result.get('success') and result.get('activities'):
        return result['activities']
    
    return st.session_state.user_activity_log


def log_user_activity(username: str, action: str, details: str = ""):
    """Log user activity to API and session."""
    # Log to session
    log = st.session_state.get('user_activity_log', [])
    log.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'username': username,
        'action': action,
        'details': details
    })
    st.session_state.user_activity_log = log
    
    # Try to log to API
    api_request('log-activity', 'POST', {
        'username': username,
        'action': action,
        'details': details
    })


def init_auth_state():
    """Initialize authentication state."""
    
    # Check for Persistent Session (Remember Me)
    if 'authenticated' not in st.session_state:
        saved_session = load_session()
        if saved_session:
             # Auto-login if session exists
            username = saved_session.get('username')
            users = get_users() # ensure users are loaded
            
            # Verify user still exists in our records
            if username in users:
                user_data = users[username]
                st.session_state.authenticated = True
                st.session_state.user = {
                    'username': username,
                    'name': user_data.get('name', username),
                    'role': user_data.get('role', 'user'),
                    'email': user_data.get('email', '')
                }
                # Silent login, no need for notification
            else:
                 # Clean up invalid session
                clear_session()
    
    # Default Guest State if still not authenticated
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = True # Temporarily True for Guest-allowed apps, BUT...
        # Note: Apps that require auth will check st.session_state.user['username'] != 'guest'
    
    if 'user' not in st.session_state:
        st.session_state.user = {
            'username': 'guest',
            'name': 'Tamu (Guest)',
            'role': 'user', 
            'email': 'guest@agrisensa.com'
        }
        
    if 'user_activity_log' not in st.session_state:
        st.session_state.user_activity_log = []
        
    get_users()


def login(username: str, password: str, remember_me: bool = False) -> tuple:
    """Authenticate user with API, fallback to session/local."""
    init_auth_state()
    
    if not username or not password:
        return False, "Username dan password harus diisi"
    
    username = username.strip().lower()
    
    # 1. Try API login first (if connected)
    result = api_request('simple-login', 'POST', {
        'username': username,
        'password': password
    })
    
    if result.get('success'):
        user_data = result.get('user', {})
        st.session_state.authenticated = True
        st.session_state.user = {
            'username': user_data.get('username', username),
            'name': user_data.get('name', username),
            'role': user_data.get('role', 'user'),
            'email': user_data.get('email', '')
        }
        if remember_me:
            save_session(username)
        return True, result.get('message', 'Login berhasil!')
    
    # 2. If API fails, try local USERS (Default + Local JSON)
    users = get_users()
    if username in users:
        if users[username]['password'] == password:
            st.session_state.authenticated = True
            st.session_state.user = {
                'username': username,
                'name': users[username]['name'],
                'role': users[username]['role'],
                'email': users[username]['email']
            }
            log_user_activity(username, 'LOGIN', 'Login via local')
            
            if remember_me:
                save_session(username)
                
            return True, f"Selamat datang, {users[username]['name']}!"
        else:
            return False, "Password salah"
    
    # 3. If not in local users either
    return False, result.get('message', f'Username {username} tidak ditemukan')


def logout():
    """Logout current user."""
    if st.session_state.get('user'):
        log_user_activity(st.session_state.user['username'], 'LOGOUT', 'User logout')
    
    # Clear session state
    st.session_state.authenticated = False
    st.session_state.user = None
    
    # Clear persistent session
    clear_session()


def register(username: str, password: str, name: str, email: str) -> tuple:
    """Register a new user via API with session+local fallback."""
    init_auth_state()
    
    if not username or not password or not name:
        return False, "Username, password, dan nama harus diisi"
    
    if len(username) < 3:
        return False, "Username minimal 3 karakter"
    
    if len(password) < 6:
        return False, "Password minimal 6 karakter"
    
    username = username.strip().lower()
    
    # 1. Try API register first
    result = api_request('simple-register', 'POST', {
        'username': username,
        'password': password,
        'name': name,
        'email': email
    })
    
    if result.get('success'):
        user_data = result.get('user', {})
        st.session_state.authenticated = True
        st.session_state.user = {
            'username': user_data.get('username', username),
            'name': user_data.get('name', name),
            'role': user_data.get('role', 'user'),
            'email': user_data.get('email', email)
        }
        return True, result.get('message', 'Registrasi berhasil!')
    
    # 2. If API error, try local fallback
    if result.get('api_error'):
        users = get_users()
        if username in users:
            return False, "Username sudah digunakan"
        
        # Create new user entry
        new_user = {
            'password': password,
            'role': 'user',
            'name': name,
            'email': email or f"{username}@agrisensa.com"
        }
        
        # Update Session State
        users[username] = new_user
        st.session_state.registered_users = users
        
        # Update Local Persistence (users.json)
        local_users = load_local_users()
        local_users[username] = new_user
        save_local_users(local_users)
        
        # Auto-login
        st.session_state.authenticated = True
        st.session_state.user = {
            'username': username,
            'name': name,
            'role': 'user',
            'email': email or f"{username}@agrisensa.com"
        }
        
        # Also save simple session for convenience if they just registered
        save_session(username) 
        
        log_user_activity(username, 'REGISTER', 'Register via local')
        return True, f"Selamat datang, {name}! Akun berhasil dibuat & disimpan."
    
    return False, result.get('message', 'Registrasi gagal')


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    init_auth_state()
    return st.session_state.authenticated


def get_current_user() -> dict:
    """Get current logged in user info."""
    init_auth_state()
    return st.session_state.user


def require_auth():
    """Require authentication to access page."""
    init_auth_state()
    
    # If not authenticated OR is guest, block access
    # (Checking user['username'] == 'guest' is important because init_auth_state defaults authenticated=True for Guest)
    current_user = st.session_state.user
    if not st.session_state.authenticated or (current_user and current_user.get('username') == 'guest'):
        show_login_required()
        st.stop()
    
    return st.session_state.user


def show_login_required():
    """Show login required message with Register option."""
    st.warning("🔐 **Akses Terbatas** - Silakan Login atau Buat Akun")
    
    tab_login, tab_register = st.tabs(["🔑 Login", "📝 Daftar Baru"])
    
    with tab_login:
        with st.form("quick_login"):
            username = st.text_input("Username", placeholder="admin / demo / petani")
            password = st.text_input("Password", type="password")
            remember_me = st.checkbox("Ingat Saya (Remember Me)")
            
            if st.form_submit_button("Masuk (Login)", use_container_width=True, type="primary"):
                success, message = login(username, password, remember_me)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    with tab_register:
        with st.form("quick_register"):
            r_user = st.text_input("Username Baru", placeholder="Min 3 karakter (contoh: budi_tani)")
            r_pass = st.text_input("Password", type="password", placeholder="Min 6 karakter")
            r_name = st.text_input("Nama Lengkap", placeholder="Budi Santoso")
            r_email = st.text_input("Email (Opsional)")
            
            if st.form_submit_button("Buat Akun", use_container_width=True):
                success, message = register(r_user, r_pass, r_name, r_email)
                if success:
                    st.success(f"✅ {message} Silakan Login.")
                else:
                    st.error(message)

    st.caption("Default: admin/admin123, petani/petani123")


def show_user_info_sidebar():
    """Show current user info in sidebar."""
    if is_authenticated():
        user = get_current_user()
        # Only show valid users, skip guest
        if user and user.get('username') != 'guest':
            role_icon = '👑' if user['role'] == 'superadmin' else ('🛡️' if user['role'] == 'admin' else '👤')
            st.sidebar.success(f"{role_icon} **{user['name']}** ({user['role']})")
            
            # LINK BUTTON BACK TO MAIN HUB
            st.sidebar.markdown("---")
            st.sidebar.link_button("🏠 Kembali ke Menu Utama", "https://mirai39.streamlit.app/", use_container_width=True)
            
            if st.sidebar.button("🚪 Logout", use_container_width=True):
                logout()
                st.rerun()
        return
