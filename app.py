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
@app.route('/api/live-data', methods=['GET'])
def get_live_data():
    try:
        # Cargamos la sesión más reciente (2026)
        session = fastf1.get_session(2025, 1, 'R')
        session.load()
        
        # Extraemos los datos necesarios para el Live Timing
        # 'Abbreviation' es el código de 3 letras (ej: VER, HAM)
        pilotos_data = session.results[['Position', 'Abbreviation', 'TeamName', 'FullName']].to_dict('records')
        
        return jsonify({"pilotos": pilotos_data})
    except Exception as e:
        # Esto nos ayuda a ver qué falla exactamente en el navegador si hay error
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Usamos el puerto que Railway nos asigna, o el 8080 por defecto
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)