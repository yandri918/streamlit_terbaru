"""
Database Connection Wrapper with Auto-Retry Logic
Handles SSL connection errors and provides robust database connectivity
"""

import time
import logging
from functools import wraps
from typing import Any, Callable, Optional
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConnectionError(Exception):
    """Custom exception for database connection issues"""
    pass


def retry_on_db_error(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator to retry database operations on connection failures
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries (seconds)
        backoff: Multiplier for delay after each retry
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                    
                except Exception as e:
                    last_exception = e
                    error_msg = str(e).lower()
                    
                    # Check if it's a retryable error
                    retryable_errors = [
                        'ssl connection has been closed',
                        'connection reset',
                        'connection refused',
                        'timeout',
                        'operationalerror',
                        'connection lost'
                    ]
                    
                    is_retryable = any(err in error_msg for err in retryable_errors)
                    
                    if not is_retryable or attempt == max_retries:
                        logger.error(f"Database error (attempt {attempt + 1}/{max_retries + 1}): {e}")
                        raise
                    
                    # Log retry attempt
                    logger.warning(
                        f"Database connection error (attempt {attempt + 1}/{max_retries + 1}): {e}. "
                        f"Retrying in {current_delay:.1f}s..."
                    )
                    
                    # Wait before retry
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            # If we get here, all retries failed
            raise DatabaseConnectionError(
                f"Failed after {max_retries + 1} attempts. Last error: {last_exception}"
            )
        
        return wrapper
    return decorator


def get_database_url() -> str:
    """
    Get database URL from Streamlit secrets or environment
    
    Returns:
        Database connection URL
    """
    try:
        # Try Streamlit secrets first
        if hasattr(st, 'secrets') and 'DATABASE_URL' in st.secrets:
            return st.secrets['DATABASE_URL']
    except Exception:
        pass
    
    # Fallback to environment variable
    import os
    db_url = os.getenv('DATABASE_URL')
    
    if not db_url:
        raise DatabaseConnectionError(
            "DATABASE_URL not found in secrets or environment variables"
        )
    
    return db_url


def create_db_engine(database_url: Optional[str] = None):
    """
    Create SQLAlchemy engine with proper connection pooling and SSL settings
    
    Args:
        database_url: Optional database URL (will auto-detect if not provided)
    
    Returns:
        SQLAlchemy engine instance
    """
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.pool import NullPool
    except ImportError:
        raise ImportError("SQLAlchemy is required. Install with: pip install sqlalchemy")
    
    if database_url is None:
        database_url = get_database_url()
    
    # Ensure SSL mode is set for PostgreSQL
    if 'postgresql' in database_url and 'sslmode' not in database_url:
        separator = '&' if '?' in database_url else '?'
        database_url = f"{database_url}{separator}sslmode=require"
    
    # Create engine with robust settings
    engine = create_engine(
        database_url,
        pool_pre_ping=True,  # Test connection before using from pool
        pool_recycle=3600,   # Recycle connections after 1 hour
        pool_size=5,         # Maximum pool size
        max_overflow=10,     # Maximum overflow connections
        connect_args={
            "connect_timeout": 10,
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        } if 'postgresql' in database_url else {},
        echo=False  # Set to True for SQL debugging
    )
    
    logger.info("Database engine created successfully")
    return engine


@retry_on_db_error(max_retries=3, delay=1.0, backoff=2.0)
def execute_query(engine, query: str, params: Optional[dict] = None):
    """
    Execute a database query with automatic retry on connection errors
    
    Args:
        engine: SQLAlchemy engine
        query: SQL query string
        params: Optional query parameters
    
    Returns:
        Query result
    """
    with engine.connect() as connection:
        result = connection.execute(query, params or {})
        return result


@retry_on_db_error(max_retries=3, delay=1.0, backoff=2.0)
def get_user_by_username(engine, username: str):
    """
    Get user by username with automatic retry
    
    Args:
        engine: SQLAlchemy engine
        username: Username to search for
    
    Returns:
        User object or None
    """
    try:
        from sqlalchemy import text
    except ImportError:
        raise ImportError("SQLAlchemy is required")
    
    query = text("""
        SELECT id, username, email, password_hash, role, is_active, 
               created_at, updated_at, full_name, phone, location, farm_size
        FROM users 
        WHERE username = :username 
        LIMIT 1
    """)
    
    with engine.connect() as connection:
        result = connection.execute(query, {"username": username})
        return result.fetchone()


# Streamlit-specific helpers
@st.cache_resource
def get_cached_db_engine():
    """
    Get cached database engine for Streamlit apps
    Uses st.cache_resource to persist across reruns
    
    Returns:
        SQLAlchemy engine instance
    """
    try:
        return create_db_engine()
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        st.error(f"⚠️ Database connection error: {e}")
        st.info("💡 Tip: Check your DATABASE_URL in Streamlit secrets")
        raise


def safe_db_operation(operation: Callable, *args, **kwargs) -> Any:
    """
    Safely execute a database operation with user-friendly error handling
    
    Args:
        operation: Function to execute
        *args, **kwargs: Arguments to pass to the operation
    
    Returns:
        Operation result or None on error
    """
    try:
        return operation(*args, **kwargs)
    except DatabaseConnectionError as e:
        st.error(f"🔌 Database Connection Error: {e}")
        st.info("Please try refreshing the page or contact support if the issue persists.")
        logger.error(f"Database operation failed: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected Error: {e}")
        logger.error(f"Unexpected error in database operation: {e}")
        return None


# Example usage in Streamlit app
if __name__ == "__main__":
    """
    Example usage:
    
    # In your Streamlit app:
    from utils.db_wrapper import get_cached_db_engine, safe_db_operation, get_user_by_username
    
    # Get engine (cached)
    engine = get_cached_db_engine()
    
    # Execute query with auto-retry
    user = safe_db_operation(get_user_by_username, engine, "username")
    
    if user:
        st.write(f"Welcome, {user.full_name}!")
    """
    print("Database wrapper module loaded successfully")
