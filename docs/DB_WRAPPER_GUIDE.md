# Database Connection Wrapper - Usage Guide

## 🎯 Purpose
Handles PostgreSQL SSL connection errors with automatic retry logic and robust connection pooling.

## 🚀 Quick Start

### 1. Update Your Auth Module

Replace direct database calls with the wrapper:

```python
# OLD (Error-prone):
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)
result = engine.execute("SELECT * FROM users WHERE username = 'test'")

# NEW (Robust):
from utils.db_wrapper import get_cached_db_engine, safe_db_operation, get_user_by_username

engine = get_cached_db_engine()
user = safe_db_operation(get_user_by_username, engine, "test")
```

### 2. Update Streamlit Secrets

Ensure your `.streamlit/secrets.toml` has:

```toml
DATABASE_URL = "postgresql://user:pass@host:5432/dbname?sslmode=require"
```

## 📚 API Reference

### `@retry_on_db_error(max_retries=3, delay=1.0, backoff=2.0)`
Decorator to retry database operations on connection failures.

**Example:**
```python
@retry_on_db_error(max_retries=5, delay=2.0)
def my_db_query(engine):
    with engine.connect() as conn:
        return conn.execute("SELECT * FROM users")
```

### `get_cached_db_engine()`
Get cached database engine (Streamlit-optimized).

**Returns:** SQLAlchemy engine instance

**Example:**
```python
engine = get_cached_db_engine()
```

### `safe_db_operation(operation, *args, **kwargs)`
Execute database operation with user-friendly error handling.

**Example:**
```python
result = safe_db_operation(get_user_by_username, engine, "john_doe")
if result:
    st.write(f"User found: {result.email}")
```

### `get_user_by_username(engine, username)`
Get user by username with automatic retry.

**Example:**
```python
user = get_user_by_username(engine, "admin")
```

## 🔧 Configuration

### Connection Pool Settings
```python
pool_pre_ping=True      # Test connection before use
pool_recycle=3600       # Recycle after 1 hour
pool_size=5             # Max pool size
max_overflow=10         # Max overflow connections
```

### SSL/Keepalive Settings
```python
connect_timeout=10
keepalives=1
keepalives_idle=30
keepalives_interval=10
keepalives_count=5
```

## 🛠️ Migration Guide

### For `utils/auth.py`:

**Before:**
```python
def authenticate_user(username, password):
    engine = create_engine(st.secrets['DATABASE_URL'])
    query = "SELECT * FROM users WHERE username = ?"
    result = engine.execute(query, username)
    return result.fetchone()
```

**After:**
```python
from utils.db_wrapper import get_cached_db_engine, safe_db_operation, get_user_by_username

def authenticate_user(username, password):
    engine = get_cached_db_engine()
    user = safe_db_operation(get_user_by_username, engine, username)
    if user and verify_password(password, user.password_hash):
        return user
    return None
```

## ⚠️ Error Handling

The wrapper handles these errors automatically:
- `SSL connection has been closed unexpectedly`
- `Connection reset by peer`
- `Connection refused`
- `Timeout errors`
- `OperationalError`

**Retry Strategy:**
- Attempt 1: Immediate
- Attempt 2: Wait 1s
- Attempt 3: Wait 2s (1s × 2.0 backoff)
- Attempt 4: Wait 4s (2s × 2.0 backoff)

## 📊 Logging

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

Logs will show:
- Connection attempts
- Retry delays
- Error details

## 🎯 Best Practices

1. **Always use `get_cached_db_engine()`** in Streamlit apps
2. **Wrap user-facing operations** with `safe_db_operation()`
3. **Use `@retry_on_db_error`** for custom database functions
4. **Set `sslmode=require`** in DATABASE_URL for PostgreSQL
5. **Monitor logs** for connection issues

## 🚨 Troubleshooting

### Error: "DATABASE_URL not found"
**Solution:** Add to `.streamlit/secrets.toml`:
```toml
DATABASE_URL = "your_database_url_here"
```

### Error: "SQLAlchemy is required"
**Solution:** Install dependencies:
```bash
pip install sqlalchemy psycopg2-binary
```

### Persistent SSL Errors
**Solution:** Check database provider status and SSL certificate validity.

## 📝 Example: Complete Auth Module

```python
# utils/auth.py
import streamlit as st
from utils.db_wrapper import get_cached_db_engine, safe_db_operation, get_user_by_username
from passlib.hash import bcrypt

def require_auth():
    """Require authentication for page access"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                engine = get_cached_db_engine()
                user = safe_db_operation(get_user_by_username, engine, username)
                
                if user and bcrypt.verify(password, user.password_hash):
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        st.stop()
    
    return st.session_state.user
```

## 🔗 Related Files
- `utils/db_wrapper.py` - Main wrapper module
- `utils/auth.py` - Authentication module (update this)
- `.streamlit/secrets.toml` - Database credentials
