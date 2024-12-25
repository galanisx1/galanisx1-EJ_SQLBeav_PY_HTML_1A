from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
db_config = {
    'host': 'sql310.infinityfree.com',
    'user': 'if0_37975979',
    'password': 'Pedro3103$A',
    'database': 'eif0_37975979_ejemplo_dreamweaver',
    'port': 3306  # Puerto predeterminado de MySQL
}

@app.route('/')
def home():
    return "El servidor está funcionando correctamente."

# Ruta para insertar datos
@app.route('/insertar', methods=['POST'])
def insertar():
    data = request.json
    nombre = data['nombre']
    edad = data['edad']
    telefono = data['telefono']
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Alumno (nombre, edad, telefono) VALUES (%s, %s, %s)", (nombre, edad, telefono))
        conn.commit()
        return jsonify({'message': 'Datos insertados correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Ruta para obtener datos
@app.route('/obtener', methods=['GET'])
def obtener():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Alumno")
        datos = cursor.fetchall()
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
