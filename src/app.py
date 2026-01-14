# app.py
from flask import Flask, jsonify, request, render_template
import pymysql
import os
import time
import traceback
from datetime import datetime

app = Flask(__name__)
SECRET_PATH = "/mnt/rds-secret"
DB_PORT = 3306

# Health check WITHOUT DB dependency
@app.route("/health")
def health():
    """Health check endpoint - no DB required"""
    return "OK", 200

# Only initialize DB if secrets exist
def init_with_db():
    """Initialize database connection only if secrets are available"""
    if not os.path.exists(SECRET_PATH):
        print("⚠️  Secret path not found - running without DB")
        return False

    try:
        wait_for_secrets()

        global DB_HOST, DB_USER, DB_PASS, DB_NAME
        DB_HOST = open(os.path.join(SECRET_PATH, "host")).read().strip()
        DB_USER = open(os.path.join(SECRET_PATH, "username")).read().strip()
        DB_PASS = open(os.path.join(SECRET_PATH, "password")).read().strip()
        DB_NAME = open(os.path.join(SECRET_PATH, "dbname")).read().strip()

        print(f"📡 Will connect to RDS: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

        try:
            init_database()
        except Exception as init_error:
            print(f"⚠️  Database init failed (will retry on /init-db): {init_error}")
            traceback.print_exc()

        return True
    except Exception as e:
        print(f"⚠️  Failed to initialize DB: {e}")
        traceback.print_exc()
        return False

def wait_for_secrets(timeout=60):
    """Wait for CSI driver to mount secrets"""
    required_files = ["host", "username", "password", "dbname"]
    start_time = time.time()

    while time.time() - start_time < timeout:
        if all(os.path.exists(os.path.join(SECRET_PATH, f)) for f in required_files):
            print("✅ All secret files found!")
            return True
        print(f"⏳ Waiting for secrets to be mounted... ({int(time.time() - start_time)}s)")
        time.sleep(2)

    raise FileNotFoundError(f"Secrets not found in {SECRET_PATH} after {timeout}s")

def get_db_connection():
    """Create database connection"""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        port=DB_PORT,
        connect_timeout=10,
        cursorclass=pymysql.cursors.DictCursor
    )

def init_database():
    """Initialize all database tables with sample data"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    finally:
        conn.close()

# Initialize DB status
DB_AVAILABLE = init_with_db()

@app.route("/")
def index():
    """RENDER THE MAP - This replaces the JSON response"""
    return render_template('index.html')

@app.route("/api/info")
def api_info():
    """The original JSON status is now moved here"""
    if not DB_AVAILABLE:
        return jsonify({
            "status": "⚠️ Running without database",
            "message": "Secrets not mounted",
            "endpoints": {"health": "/health", "map": "/"}
        }), 200
    
    return jsonify({"status": "✅ Connected to RDS!"}), 200

# Keep your other endpoints (users, products, etc.) as they were...
@app.route("/users")
def get_users():
    if not DB_AVAILABLE:
        return jsonify({"status": "error", "error": "Database not available"}), 503
    # ... logic continues here ...
    return jsonify({"users": []})

if __name__ == "__main__":
    print("🚀 Starting Flask app...")
    # Port 8080 for OpenShift
    app.run(host="0.0.0.0", port=8080, debug=True)
