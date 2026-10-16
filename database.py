import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Faltan SUPABASE_URL o SUPABASE_KEY en el archivo .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ============================================================
# USUARIOS
# ============================================================

def crear_usuario(email: str, nombre: str, rol: str, telefono: str = None, whatsapp: str = None):
    data = {"email": email, "nombre": nombre, "rol": rol, "telefono": telefono, "whatsapp": whatsapp}
    return supabase.table("usuarios").insert(data).execute()


def obtener_usuario_por_email(email: str):
    respuesta = supabase.table("usuarios").select("*").eq("email", email).execute()
    if respuesta.data:
        return respuesta.data[0]
    return None


def obtener_usuario_por_id(usuario_id: int):
    respuesta = supabase.table("usuarios").select("*").eq("id", usuario_id).execute()
    if respuesta.data:
        return respuesta.data[0]
    return None


# ============================================================
# CATEGORIAS
# ============================================================

def listar_categorias():
    respuesta = supabase.table("categorias").select("*").eq("activo", True).order("nombre").execute()
    return respuesta.data


def listar_categorias_arbol():
    """Devuelve las categorias organizadas en estructura de arbol."""
    todas = listar_categorias()
    # Crear un diccionario por id
    por_id = {c["id"]: {**c, "hijos": []} for c in todas}
    raices = []
    for c in por_id.values():
        padre_id = c.get("padre_id")
        if padre_id and padre_id in por_id:
            por_id[padre_id]["hijos"].append(c)
        else:
            raices.append(c)
    return raices


def obtener_descendientes(categoria_id: int):
    """Devuelve TODAS las categorias descendientes (incluyendo la propia)."""
    todas = listar_categorias()
    resultado = [categoria_id]
    # Buscar hijos recursivamente
    cambio = True
    while cambio:
        cambio = False
        for c in todas:
            if c.get("padre_id") in resultado and c["id"] not in resultado:
                resultado.append(c["id"])
                cambio = True
    return resultado


def obtener_ancestros(categoria_id: int):
    """Devuelve la categoria y todos sus ancestros hacia arriba."""
    todas = listar_categorias()
    por_id = {c["id"]: c for c in todas}
    resultado = [categoria_id]
    actual = por_id.get(categoria_id)
    while actual and actual.get("padre_id"):
        padre = por_id.get(actual["padre_id"])
        if padre:
            resultado.append(padre["id"])
            actual = padre
        else:
            break
    return resultado


def crear_categoria(nombre: str, padre_id: Optional[int] = None, tipo: str = None):
    data = {"nombre": nombre, "padre_id": padre_id, "tipo": tipo}
    return supabase.table("categorias").insert(data).execute()


def eliminar_categoria(categoria_id: int):
    """Desactiva una categoria (soft delete)."""
    supabase.table("categorias").update({"activo": False}).eq("id", categoria_id).execute()
    return {"ok": True, "categoria_id": categoria_id}


# ============================================================
# SOLICITUDES
# ============================================================

def crear_solicitud(cliente_id: int, categoria_id: int, titulo: str,
                    descripcion: str = None, ubicacion: str = None,
                    radio_busqueda: int = None):
    """Crea una solicitud Y notifica a proveedores suscritos a esa categoria O a cualquier ancestro."""
    data = {
        "cliente_id": cliente_id, "categoria_id": categoria_id,
        "titulo": titulo, "descripcion": descripcion,
        "ubicacion": ubicacion, "radio_busqueda": radio_busqueda,
    }
    resultado = supabase.table("solicitudes").insert(data).execute()

    if resultado.data:
        solicitud_id = resultado.data[0]["id"]
        try:
            # Obtener ancestros de la categoria
            categorias_relevantes = obtener_ancestros(categoria_id)

            # Buscar proveedores suscritos a cualquier ancestro
            proveedores_ids = set()
            for cat_id in categorias_relevantes:
                resp = supabase.table("proveedor_categorias").select("proveedor_id").eq("categoria_id", cat_id).execute()
                for p in resp.data:
                    proveedores_ids.add(p["proveedor_id"])

            # Crear notificaciones
            for proveedor_id in proveedores_ids:
                try:
                    supabase.table("notificaciones").insert({
                        "usuario_id": proveedor_id,
                        "solicitud_id": solicitud_id,
                    }).execute()
                except Exception:
                    pass
        except Exception as e:
            print(f"Advertencia notificaciones: {e}")

    return resultado


def listar_solicitudes():
    respuesta = supabase.table("solicitudes").select("*").order("fecha_creacion", desc=True).execute()
    return respuesta.data


def listar_solicitudes_de_cliente(cliente_id: int):
    respuesta = (supabase.table("solicitudes").select("*")
                 .eq("cliente_id", cliente_id).order("fecha_creacion", desc=True).execute())
    return respuesta.data


def obtener_solicitud(solicitud_id: int):
    respuesta = supabase.table("solicitudes").select("*").eq("id", solicitud_id).execute()
    if respuesta.data:
        return respuesta.data[0]
    return None


def cancelar_solicitud(solicitud_id: int):
    supabase.table("solicitudes").update({"estado": "cancelada"}).eq("id", solicitud_id).execute()
    return {"ok": True, "solicitud_id": solicitud_id}


def cerrar_solicitud(solicitud_id: int):
    ofertas = supabase.table("ofertas").select("*").eq("solicitud_id", solicitud_id).execute()
    if not ofertas.data:
        raise ValueError("No hay ofertas en esta solicitud")
    aceptada = next((o for o in ofertas.data if o["estado"] == "aceptada"), None)
    if not aceptada:
        raise ValueError("No hay oferta aceptada")
    supabase.table("ofertas").update({"estado": "rechazada"}).eq("solicitud_id", solicitud_id).neq("id", aceptada["id"]).execute()
    supabase.table("solicitudes").update({"estado": "finalizada"}).eq("id", solicitud_id).execute()
    return {"ok": True, "solicitud_id": solicitud_id}


# ============================================================
# OFERTAS
# ============================================================

def crear_oferta(solicitud_id: int, proveedor_id: int, mensaje: str, precio: float = None):
    data = {"solicitud_id": solicitud_id, "proveedor_id": proveedor_id, "mensaje": mensaje, "precio": precio}
    return supabase.table("ofertas").insert(data).execute()


def listar_ofertas_de_solicitud(solicitud_id: int):
    respuesta = supabase.table("ofertas").select("*").eq("solicitud_id", solicitud_id).execute()
    return respuesta.data


def listar_ofertas_con_proveedor(solicitud_id: int):
    respuesta = (supabase.table("ofertas")
                 .select("*, proveedor:usuarios!proveedor_id(id, nombre, email, telefono, whatsapp)")
                 .eq("solicitud_id", solicitud_id).execute())
    return respuesta.data


def aceptar_oferta(oferta_id: int):
    oferta_resp = supabase.table("ofertas").select("*").eq("id", oferta_id).execute()
    if not oferta_resp.data:
        raise ValueError("Oferta no encontrada")
    oferta = oferta_resp.data[0]
    solicitud_id = oferta["solicitud_id"]
    supabase.table("ofertas").update({"estado": "pendiente"}).eq("solicitud_id", solicitud_id).eq("estado", "aceptada").execute()
    supabase.table("ofertas").update({"estado": "aceptada"}).eq("id", oferta_id).execute()
    supabase.table("solicitudes").update({"estado": "asignada"}).eq("id", solicitud_id).execute()
    return {"ok": True, "solicitud_id": solicitud_id, "oferta_id": oferta_id}


def cancelar_aceptacion(oferta_id: int):
    oferta_resp = supabase.table("ofertas").select("*").eq("id", oferta_id).execute()
    if not oferta_resp.data:
        raise ValueError("Oferta no encontrada")
    oferta = oferta_resp.data[0]
    solicitud_id = oferta["solicitud_id"]
    supabase.table("ofertas").update({"estado": "pendiente"}).eq("id", oferta_id).execute()
    supabase.table("solicitudes").update({"estado": "con_ofertas"}).eq("id", solicitud_id).execute()
    return {"ok": True, "solicitud_id": solicitud_id, "oferta_id": oferta_id}


# ============================================================
# NOTIFICACIONES
# ============================================================

def crear_notificacion(usuario_id: int, solicitud_id: int):
    data = {"usuario_id": usuario_id, "solicitud_id": solicitud_id}
    return supabase.table("notificaciones").insert(data).execute()


def listar_notificaciones(usuario_id: int, solo_no_leidas: bool = False):
    query = supabase.table("notificaciones").select("*").eq("usuario_id", usuario_id)
    if solo_no_leidas:
        query = query.eq("leida", False)
    return query.order("fecha_creacion", desc=True).execute().data


def contar_notificaciones_no_leidas(usuario_id: int):
    respuesta = (supabase.table("notificaciones").select("id", count="exact")
                 .eq("usuario_id", usuario_id).eq("leida", False).execute())
    return respuesta.count or 0


def marcar_notificacion_leida(notificacion_id: int):
    supabase.table("notificaciones").update({"leida": True}).eq("id", notificacion_id).execute()
    return {"ok": True, "notificacion_id": notificacion_id}


def marcar_todas_leidas(usuario_id: int):
    supabase.table("notificaciones").update({"leida": True}).eq("usuario_id", usuario_id).eq("leida", False).execute()
    return {"ok": True, "usuario_id": usuario_id}


def listar_notificaciones_detalladas(usuario_id: int, solo_no_leidas: bool = False):
    query = (supabase.table("notificaciones")
             .select("*, solicitud:solicitudes!solicitud_id(id, titulo, descripcion, ubicacion, estado, fecha_creacion)")
             .eq("usuario_id", usuario_id))
    if solo_no_leidas:
        query = query.eq("leida", False)
    return query.order("fecha_creacion", desc=True).execute().data


# ============================================================
# PROVEEDOR_CATEGORIAS
# ============================================================

def listar_categorias_de_proveedor(proveedor_id: int):
    """Devuelve las categorias suscritas por un proveedor."""
    respuesta = (supabase.table("proveedor_categorias")
                 .select("categoria_id, categorias:categoria_id(id, nombre, padre_id)")
                 .eq("proveedor_id", proveedor_id).execute())
    return [r["categorias"] for r in respuesta.data if r.get("categorias")]


def agregar_categoria_a_proveedor(proveedor_id: int, categoria_id: int):
    try:
        supabase.table("proveedor_categorias").insert({
            "proveedor_id": proveedor_id,
            "categoria_id": categoria_id,
        }).execute()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def quitar_categoria_de_proveedor(proveedor_id: int, categoria_id: int):
    supabase.table("proveedor_categorias")\
        .delete()\
        .eq("proveedor_id", proveedor_id)\
        .eq("categoria_id", categoria_id)\
        .execute()
    return {"ok": True}
# ============================================================
# AUTENTICACION (Supabase Auth)
# ============================================================

def registrar_usuario_auth(email: str, password: str, nombre: str, rol: str,
                            telefono: str = None, whatsapp: str = None):
    """
    Registra un usuario en Supabase Auth Y crea el registro en la tabla usuarios.
    Devuelve los datos del usuario creado (sin password).
    """
    try:
        # 1. Crear el usuario en Supabase Auth
        auth_resp = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        if not auth_resp.user:
            raise ValueError("No se pudo crear el usuario en Auth")

        auth_id = auth_resp.user.id

        # 2. Crear el registro en la tabla usuarios
        data = {
            "auth_id": auth_id,
            "email": email,
            "nombre": nombre,
            "rol": rol,
            "telefono": telefono,
            "whatsapp": whatsapp,
            "email_verificado": False,
        }
        resp = supabase.table("usuarios").insert(data).execute()

        # 3. Cerrar la sesion temporal que creo sign_up
        supabase.auth.sign_out()

        return {
            "ok": True,
            "auth_id": auth_id,
            "usuario": resp.data[0] if resp.data else None,
            "mensaje": "Revisa tu correo para confirmar la cuenta",
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def iniciar_sesion(email: str, password: str):
    """
    Inicia sesion con email y password. Devuelve el access_token y datos del usuario.
    """
    try:
        auth_resp = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        if not auth_resp.session:
            return {"ok": False, "error": "Credenciales invalidas"}

        access_token = auth_resp.session.access_token
        auth_id = auth_resp.user.id

        # Buscar el usuario en la tabla
        resp = supabase.table("usuarios").select("*").eq("auth_id", auth_id).execute()
        if not resp.data:
            return {"ok": False, "error": "Usuario no encontrado en la base de datos"}

        usuario = resp.data[0]

        # Cerrar la sesion global del cliente (usaremos el token explicitamente)
        supabase.auth.sign_out()

        return {
            "ok": True,
            "access_token": access_token,
            "usuario": usuario,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def obtener_usuario_por_token(access_token: str):
    """
    Dado un access_token (JWT), devuelve el usuario de la tabla usuarios.
    Se usa en cada peticion para saber quien esta logueado.
    """
    try:
        auth_resp = supabase.auth.get_user(access_token)
        if not auth_resp.user:
            return None
        auth_id = auth_resp.user.id
        resp = supabase.table("usuarios").select("*").eq("auth_id", auth_id).execute()
        if resp.data:
            return resp.data[0]
        return None
    except Exception:
        return None


def cerrar_sesion_usuario():
    """Cierra la sesion global del cliente Supabase (limpieza)."""
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    return {"ok": True}


def verificar_email_usuario(auth_id: str):
    """Marca el email como verificado en la tabla usuarios."""
    try:
        supabase.table("usuarios").update({"email_verificado": True}).eq("auth_id", auth_id).execute()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}