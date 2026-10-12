Los archivos modificados son:
- database.py
- app.py 

Los cambios realizados fueron la creación del archivo database.py y su respectiva función insert_solicitud para conexión con Supabase y la modificación del endpoint /solicitud en app.py, el cual espera la solicitud entrante, invoca la función insert_solicitud y retorna la confirmación de inserción o error.