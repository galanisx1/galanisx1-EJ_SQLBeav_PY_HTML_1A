import os
from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    'host': 'sql310.infinityfree.com',
    'user': 'if0_37975979',
    'password': 'Pedro3103$A',
    'database': 'eif0_37975979_ejemplo_dreamweaver',
    'port': 3306
}

# Basic route to test server
@app.route('/')
def home():
    return "El servidor está funcionando correctamente."

# Test route without database
@app.route('/test')
def test():
    return jsonify({"status": "Server is working"}), 200

# Insert route
@app.route('/insertar', methods=['POST'])
def insertar_datos():  # Changed function name to avoid potential conflicts
    data = request.json
    nombre = data['nombre']
    edad = data['edad']
    telefono = data['telefono']
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Alumno (nombre, edad, telefono) VALUES (%s, %s, %s)", 
                      (nombre, edad, telefono))
        conn.commit()
        return jsonify({'message': 'Datos insertados correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Get route
@app.route('/obtener', methods=['GET'])
def obtener_datos():  # Changed function name to avoid potential conflicts
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Alumno")
        datos = cursor.fetchall()
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Run the app
if __name__ == '__main__':
    port = int(os.getenv("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
