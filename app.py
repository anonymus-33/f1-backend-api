from flask import Flask, render_template, jsonify
from flask_cors import CORS
import fastf1
import os

app = Flask(__name__)
CORS(app)

# Configuramos fastf1 para evitar errores de caché en producción
fastf1.Cache.enable_cache('/tmp')

@app.route('/')
def index():
    return render_template('f1.html')

@app.route('/api/live-data')
def get_live_data():
    try:
        # Cargar la sesión más reciente
        session = fastf1.get_session(2026, 'latest', 'R')
        session.load()
        
        # Obtenemos los resultados básicos
        pilotos = session.results[['Abbreviation', 'TeamName', 'FullName', 'Position']].to_dict('records')
        
        return jsonify({"pilotos": pilotos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)