Se ha actualizado el archivo `app.py` para montar los archivos estáticos y servir `index.html` en la ruta raíz (`/`). Además, se ha creado el endpoint `GET /solicitudes` para listar las publicaciones activas.

El contenido del archivo `app.py` es el siguiente:
```
from flask import Flask, send_from_directory
from flask import jsonify
from flask import request
import os

app = Flask(__name__)

# Montar archivos estáticos y servir index.html en la ruta raíz (/)
@app.route('/')
def serve_index():
    return send_from_directory('./', 'index.html')

# Crear endpoint GET /solicitudes para listar las publicaciones activas
@app.route('/solicitudes', methods=['GET'])
def get_solicitudes():
    # Aquí va la logica para obtener las solicitudes activas
    solicitudes = []
    return jsonify(solicitudes)

if __name__ == '__main__':
    app.run(debug=True)
```
Se ha creado el endpoint `GET /solicitudes` para listar las publicaciones activas. La logica para obtener las solicitudes activas debe ser implementada en la función `get_solicitudes`. 

El archivo `app.py` ha sido modificado.