import os
from flask import Flask, jsonify
from flask_cors import CORS
import fastf1

app = Flask(__name__)
CORS(app)

# Cacheamos los datos para no descargar lo mismo cada vez
# fastf1.Cache.enable_cache('cache') 

@app.route('/api/pilotos', methods=['GET'])
def get_pilotos():
    try:
        session = fastf1.get_session(2026, 'latest', 'R')
        session.load()
        pilotos = session.results[['FullName', 'TeamName', 'Position']].to_dict('records')
        return jsonify(pilotos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # ESTO ES LO QUE ARREGLA EL CRASH:
    port = int(os.environ.get('PORT', 5000)) 
    app.run(host='0.0.0.0', port=port)