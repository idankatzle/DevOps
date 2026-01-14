from flask import Flask, jsonify, request, render_template
import pymysql
import os
import time
import traceback
from datetime import datetime

app = Flask(__name__)
SECRET_PATH = "/mnt/rds-secret"
DB_PORT = 3306

@app.route("/health")
def health():
    return "OK", 200

def init_with_db():
    if not os.path.exists(SECRET_PATH):
        print("⚠️ Secret path not found - running without DB")
        return False
    try:
        # Wait for secrets and initialize
        global DB_HOST, DB_USER, DB_PASS, DB_NAME
        DB_HOST = open(os.path.join(SECRET_PATH, "host")).read().strip()
        DB_USER = open(os.path.join(SECRET_PATH, "username")).read().strip()
        DB_PASS = open(os.path.join(SECRET_PATH, "password")).read().strip()
        DB_NAME = open(os.path.join(SECRET_PATH, "dbname")).read().strip()
        return True
    except:
        return False

# Initialize status
DB_AVAILABLE = init_with_db()

@app.route("/")
def index():
    # THIS LINE RESTORES THE VISUAL MAP
    return render_template('index.html')

@app.route("/api/status")
def status():
    return jsonify({
        "status": "Running",
        "db_connected": DB_AVAILABLE
    })

# Add your existing endpoints here if needed (users, products, etc.)

if __name__ == "__main__":
    print("🚀 Starting Flask app on port 8080...")
    app.run(host="0.0.0.0", port=8080, debug=True)
