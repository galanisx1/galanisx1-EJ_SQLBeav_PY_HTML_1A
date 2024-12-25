import os
from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_config = {
    'host': '185.27.134.10',
    'user': 'if0_37975979',
    'password': 'Pedro3103$A',
    'database': 'eif0_37975979_ejemplo_dreamweaver',
    'port': 3306
}

@app.route('/')
def home():
    return jsonify({"message": "El servidor está funcionando correctamente."})

@app.route('/obtener', methods=['GET'])
def obtener_datos():
    try:
        logger.info("Attempting database connection...")
        conn = mysql.connector.connect(**db_config)
        logger.info("Database connection successful")
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Alumno")
        datos = cursor.fetchall()
        logger.info(f"Retrieved {len(datos)} records")
        
        return jsonify(datos), 200
        
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        return jsonify({
            'error': 'Database connection error',
            'details': str(err)
        }), 500
    except Exception as e:
        logger.error(f"General error: {e}")
        return jsonify({
            'error': 'Server error',
            'details': str(e)
        }), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            logger.info("Database connection closed")

@app.route('/insertar', methods=['POST'])
def insertar_datos():
    try:
        data = request.json
        logger.info(f"Received data: {data}")
        
        required_fields = ['nombre', 'edad', 'telefono']
        if not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required fields',
                'required': required_fields
            }), 400
            
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO Alumno (nombre, edad, telefono) VALUES (%s, %s, %s)",
            (data['nombre'], data['edad'], data['telefono'])
        )
        
        conn.commit()
        logger.info("Data inserted successfully")
        
        return jsonify({
            'message': 'Datos insertados correctamente',
            'inserted_data': data
        }), 200
        
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        return jsonify({
            'error': 'Database error',
            'details': str(err)
        }), 500
    except Exception as e:
        logger.error(f"General error: {e}")
        return jsonify({
            'error': 'Server error',
            'details': str(e)
        }), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    port = int(os.getenv("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
