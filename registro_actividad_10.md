Se han creado/actualizado los siguientes archivos:

- index.html
- app.py

Contenido de index.html:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QuienLoTiene</title>
    <link rel="stylesheet" href="https://cdn.tailwindcss.com">
</head>
<body>
    <h1 class="text-3xl font-bold">QuienLoTiene</h1>
    <div class="container mx-auto p-4 pt-6 mt-10">
        <div class="grid grid-cols-1 gap-4">
            <div class="card bg-gray-100">
                <h2 class="text-xl font-bold">Solicitud 1</h2>
                <p>Descripcion de la solicitud 1</p>
            </div>
            <div class="card bg-gray-100">
                <h2 class="text-xl font-bold">Solicitud 2</h2>
                <p>Descripcion de la solicitud 2</p>
            </div>
        </div>
    </div>
    <button id="modal-btn" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Oferta</button>
    <div id="modal" class="hidden">
        <div class="bg-gray-100">
            <h2 class="text-xl font-bold">Oferta</h2>
            <p>Descripcion de la oferta</p>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvp4DGHobzQ" crossorigin="anonymous"></script>
</body>
</html>
```

Contenido de app.py:
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