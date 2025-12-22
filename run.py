from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from app import create_app

app = create_app()

if __name__ == '__main__':
    # For local development
    print("=" * 60)
    print("🚀 Starting AgriSensa API Server")
    print("=" * 60)
    print("📍 Server running at: http://localhost:5000")
    print("📊 Health check: http://localhost:5000/health")
    print("📖 API info: http://localhost:5000/api/info")
    print("🏠 Home page: http://localhost:5000/")
    print("=" * 60)
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
