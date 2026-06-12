from flask import Flask, jsonify
from flask_cors import CORS
import fastf1

app = Flask(__name__)
CORS(app)  # Esto permite que tu web en Vercel se conecte a este servidor

# Cacheamos los datos para no descargar lo mismo cada vez
fastf1.Cache.enable_cache('cache') 

@app.route('/api/pilotos', methods=['GET'])
def get_pilotos():
    try:
        # Cargamos la última carrera disponible (2026)
        session = fastf1.get_session(2026, 'latest', 'R')
        session.load()
        
        # Obtenemos los resultados y convertimos a lista de diccionarios
        pilotos = session.results[['FullName', 'TeamName', 'Position']].to_dict('records')
        return jsonify(pilotos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)