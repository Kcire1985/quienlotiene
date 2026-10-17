"""
Herramientas personalizadas para el agente OTC de QuienLoTiene.
- Consultas de solo lectura a Supabase
- Busqueda web gratuita (DuckDuckGo)
- Envio de correos electronicos (Resend)
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from crewai.tools import tool
from duckduckgo_search import DDGS
import resend
from resend.exceptions import ResendError

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Faltan SUPABASE_URL o SUPABASE_KEY en .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Solo estas tablas se pueden consultar
TABLAS_PERMITIDAS = [
    "usuarios",
    "categorias",
    "proveedor_categorias",
    "solicitudes",
    "ofertas",
    "notificaciones",
]


# ============================================================
# HERRAMIENTA 1 - Listar tablas
# ============================================================

@tool("Listar tablas disponibles en la base de datos")
def listar_tablas() -> str:
    """Devuelve la lista de tablas que existen en la base de datos de QuienLoTiene."""
    return (
        "Tablas disponibles: "
        + ", ".join(TABLAS_PERMITIDAS)
        + ". Usa 'Consultar tabla Supabase' para ver los datos de una."
    )


# ============================================================
# HERRAMIENTA 2 - Consultar tabla (solo lectura)
# ============================================================

@tool("Consultar tabla Supabase (solo lectura)")
def consultar_tabla(tabla: str, limite: int = 20) -> str:
    """
    Consulta las primeras N filas de una tabla. Solo lectura.
    Args:
        tabla: nombre de la tabla (usuarios, categorias, solicitudes, ofertas, etc.)
        limite: numero maximo de filas a devolver (default 20)
    """
    if tabla not in TABLAS_PERMITIDAS:
        return f"Tabla '{tabla}' no permitida. Disponibles: {', '.join(TABLAS_PERMITIDAS)}"
    try:
        resp = supabase.table(tabla).select("*").limit(limite).execute()
        total = len(resp.data)
        if total == 0:
            return f"La tabla '{tabla}' esta vacia."
        return f"Tabla '{tabla}' ({total} filas):\n{resp.data}"
    except Exception as e:
        return f"Error consultando '{tabla}': {str(e)}"


# ============================================================
# HERRAMIENTA 3 - Contar filas
# ============================================================

@tool("Contar filas de una tabla Supabase")
def contar_filas(tabla: str) -> str:
    """
    Cuenta cuantas filas tiene una tabla. Util para estadisticas rapidas.
    Args:
        tabla: nombre de la tabla
    """
    if tabla not in TABLAS_PERMITIDAS:
        return f"Tabla '{tabla}' no permitida."
    try:
        resp = supabase.table(tabla).select("id", count="exact").execute()
        return f"Tabla '{tabla}': {resp.count} filas."
    except Exception as e:
        return f"Error contando '{tabla}': {str(e)}"


# ============================================================
# HERRAMIENTA 4 - Buscar en web (DuckDuckGo, gratis)
# ============================================================

@tool("Buscar informacion en internet")
def buscar_web(consulta: str) -> str:
    """
    Busca informacion actualizada en internet usando DuckDuckGo.
    Util para documentacion tecnica, tendencias, noticias o datos recientes.
    Args:
        consulta: terminos de busqueda en español o ingles
    """
    try:
        resultados = []
        with DDGS() as ddgs:
            for i, r in enumerate(ddgs.text(consulta, max_results=5), 1):
                resultados.append(
                    f"{i}. {r.get('title', 'Sin titulo')}\n"
                    f"   {r.get('body', 'Sin descripcion')}\n"
                    f"   Fuente: {r.get('href', '')}"
                )
        if not resultados:
            return f"Sin resultados para '{consulta}'."
        return f"Resultados para '{consulta}':\n\n" + "\n\n".join(resultados)
    except Exception as e:
        return f"Error en busqueda web: {str(e)}"


# ============================================================
# HERRAMIENTA 5 - Enviar correo electronico (Resend)
# ============================================================

@tool("Enviar correo electronico a un usuario")
def enviar_email(destinatario: str, asunto: str, cuerpo_html: str) -> str:
    """
    Envia un correo electronico usando Resend.
    Args:
        destinatario: direccion de correo del destinatario
        asunto: asunto del correo
        cuerpo_html: contenido del correo en formato HTML
    """
    try:
        resend.api_key = os.getenv("RESEND_API_KEY")
        if not resend.api_key:
            return "Error: Falta RESEND_API_KEY en el archivo .env"

        params = {
            "from": "QuienLoTiene <no-reply@envios.quienlotiene.net>",
            "to": [destinatario],
            "subject": asunto,
            "html": cuerpo_html,
        }

        email = resend.Emails.send(params)
        return f"Correo enviado con exito. ID: {email.get('id', 'N/A')}"

    except ResendError as e:
        return f"Error de Resend: {str(e)}"
    except Exception as e:
        return f"Error inesperado al enviar correo: {str(e)}"


# ============================================================
# LISTA EXPORTABLE
# ============================================================

herramientas_otc = [
    listar_tablas,
    consultar_tabla,
    contar_filas,
    buscar_web,
    enviar_email,
]