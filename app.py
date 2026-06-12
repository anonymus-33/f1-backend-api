import os
import fastf1
from flask import Flask, jsonify, render_template
from flask_cors import CORS

# Inicialización de la aplicación
app = Flask(__name__)
CORS(app)

# Configuración de caché para evitar errores de permisos en Railway
# Usamos '/tmp' porque es la única carpeta donde tenemos permiso de escritura
fastf1.Cache.enable_cache('/tmp')

# Ruta para la página principal (el dashboard)
@app.route('/')
def index():
    return render_template('f1.html')

# Ruta de la API para obtener los datos de la sesión
@app.route('/api/live-data/<string:session_type>')
def get_live_data(session_type):
    try:
        # Ahora session_type será 'FP1', 'FP2', 'Q' o 'R'
        session = fastf1.get_session(2026, 'latest', session_type)
        session.load()
        
        # Obtenemos resultados. En prácticas, a veces no hay 'Position' exacta,
        # así que usamos 'LapTime' o simplemente el orden de la tabla.
        data = session.results[['Abbreviation', 'TeamName', 'FullName']].to_dict('records')
        return jsonify({"pilotos": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Usamos el puerto que Railway nos asigna, o el 8080 por defecto
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)