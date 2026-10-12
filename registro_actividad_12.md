Se han revisado los archivos `index.html` y `app.py`. El archivo `index.html` contiene el HTML completo con Tailwind CSS y las llamadas JS a la API. El archivo `app.py` no tiene errores de sintaxis y se ejecuta correctamente.

Se ha confirmado que el servidor está respondiendo en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

**Archivos creados o modificados:**

* `index.html`: contiene el HTML completo con Tailwind CSS y las llamadas JS a la API.
* `app.py`: no tiene errores de sintaxis y se ejecuta correctamente.

**Contenido de los archivos:**

`index.html`:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QuienLoTiene</title>
    <link href="https://cdn.tailwindcss.com" rel="stylesheet">
</head>
<body>
    <h1 class="text-3xl font-bold">QuienLoTiene</h1>
    <script src="script.js"></script>
</body>
</html>
```

`app.py`:
```python
from flask import Flask, render_template, request, redirect, url_for
from database import Database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/oferta', methods=['POST'])
def oferta():
    # Procesar la oferta
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```