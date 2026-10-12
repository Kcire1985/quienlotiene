Se han creado los siguientes archivos:

1. `.env.example` con el contenido:
```
SUPABASE_URL=
SUPABASE_KEY=
```
2. `test_integration.py` con el contenido:
```python
import requests
import os
import json

# Cargar variables de entorno desde .env.example
from dotenv import load_dotenv
load_dotenv('.env.example')

# Configuración de la petición POST
url = os.getenv('SUPABASE_URL') + '/rest/v1/test'
datos = {'nombre': 'Prueba', 'descripcion': 'Registro de prueba'}
headers = {'Authorization': 'Bearer ' + os.getenv('SUPABASE_KEY'), 'Content-Type': 'application/json'}

# Realizar la petición POST
response = requests.post(url, data=json.dumps(datos), headers=headers)

# Verificar que el registro se guardó correctamente
if response.status_code == 201:
    print('Registro creado correctamente')
else:
    print('Error al crear el registro')
    print(response.text)
```
Es importante mencionar que es necesario reemplazar los valores de `SUPABASE_URL` y `SUPABASE_KEY` en el archivo `.env.example` con los valores correspondientes a la base de datos de Supabase.