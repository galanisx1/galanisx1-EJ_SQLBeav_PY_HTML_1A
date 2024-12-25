Copyimport os
from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Database configuration
db_config = {
    'host': 'sql310.infinityfree.com',
    'user': 'if0_37975979',
    'password': 'Pedro3103$A',
    'database': 'eif0_37975979_ejemplo_dreamweaver',
    'port': 3306
}

@app.route('/')
def home():
    app.logger.info("Home endpoint accessed")
    return jsonify({"message": "El servidor está funcionando correctamente."}), 200

@app.route('/test-db')
def test_db():
    try:
        app.logger.info("Testing database connection...")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        app.logger.info("Database connection successful")
        return jsonify({"status": "Database connection successful"}), 200
    except Exception as e:
        app.logger.error(f"Database connection failed: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Your existing routes...

@app.errorhandler(500)
def handle_500_error(e):
    app.logger.error(f"Internal server error: {str(e)}")
    return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.errorhandler(404)
def handle_404_error(e):
    app.logger.error(f"Page not found: {str(e)}")
    return jsonify({"error": "Route not found"}), 404

if __name__ == '__main__':
    port = int(os.getenv("PORT", 10000))
    app.logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)
