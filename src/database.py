import json
from supabase import create_client, Client
SUPABASE_URL = 'https://your-supabase-url.supabase.co'
SUPABASE_KEY = 'your-supabase-key'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_solicitud(data):
    data = json.loads(data)
    try:
        supabase.from_('solicitudes').insert([data])
        return 'Solicitud insertada correctamente'
    except Exception as e:
        return str(e)