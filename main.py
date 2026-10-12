import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import database as db

load_dotenv()

app = FastAPI(title="QuienLoTiene API")
templates = Jinja2Templates(directory="templates")


# ============================================================
# PAGINAS HTML
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/registro", response_class=HTMLResponse)
async def pagina_registro(request: Request):
    return templates.TemplateResponse(request=request, name="registro.html")


@app.get("/proveedor", response_class=HTMLResponse)
async def pagina_proveedor(request: Request):
    return templates.TemplateResponse(request=request, name="proveedor.html")


@app.get("/mis-solicitudes", response_class=HTMLResponse)
async def pagina_mis_solicitudes(request: Request):
    return templates.TemplateResponse(request=request, name="mis-solicitudes.html")


@app.get("/admin/categorias", response_class=HTMLResponse)
async def pagina_admin_categorias(request: Request):
    return templates.TemplateResponse(request=request, name="admin-categorias.html")


# ============================================================
# ENDPOINTS API - USUARIOS
# ============================================================

@app.post("/api/usuarios")
async def api_crear_usuario(
    email: str = Form(...), nombre: str = Form(...), rol: str = Form(...),
    telefono: Optional[str] = Form(None), whatsapp: Optional[str] = Form(None),
):
    try:
        resultado = db.crear_usuario(email, nombre, rol, telefono, whatsapp)
        return {"ok": True, "usuario": resultado.data}
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})


@app.get("/api/usuarios/{usuario_id}")
async def api_obtener_usuario(usuario_id: int):
    usuario = db.obtener_usuario_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"usuario": usuario}


# ============================================================
# ENDPOINTS API - CATEGORIAS
# ============================================================

@app.get("/api/categorias")
async def api_listar_categorias():
    return {"categorias": db.listar_categorias()}


@app.get("/api/categorias/arbol")
async def api_categorias_arbol():
    """Devuelve las categorias en estructura de arbol."""
    return {"arbol": db.listar_categorias_arbol()}


@app.post("/api/categorias")
async def api_crear_categoria(
    nombre: str = Form(...),
    padre_id: Optional[str] = Form(None),
    tipo: Optional[str] = Form(None),
):
    try:
        padre_int = int(padre_id) if padre_id and padre_id.strip() else None
        resultado = db.crear_categoria(nombre, padre_int, tipo)
        return {"ok": True, "categoria": resultado.data}
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})


@app.delete("/api/categorias/{categoria_id}")
async def api_eliminar_categoria(categoria_id: int):
    try:
        return db.eliminar_categoria(categoria_id)
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})


# ============================================================
# ENDPOINTS API - SOLICITUDES
# ============================================================

@app.post("/api/solicitudes")
async def api_crear_solicitud(
    cliente_id: int = Form(...), categoria_id: int = Form(...),
    titulo: str = Form(...), descripcion: Optional[str] = Form(None),
    ubicacion: Optional[str] = Form(None), radio_busqueda: Optional[int] = Form(None),
):
    try:
        resultado = db.crear_solicitud(cliente_id, categoria_id, titulo, descripcion, ubicacion, radio_busqueda)
        return {"ok": True, "solicitud": resultado.data}
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})


@app.get("/api/solicitudes")
async def api_listar_solicitudes():
    return {"solicitudes": db.listar_solicitudes()}


@app.get("/api/solicitudes/{solicitud_id}")
async def api_obtener_solicitud(solicitud_id: int):
    solicitud = db.obtener_solicitud(solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return {"solicitud": solicitud}


@app.get("/api/solicitudes/cliente/{cliente_id}")
async def api_solicitudes_de_cliente(cliente_id: int):
    return {"solicitudes": db.listar_solicitudes_de_cliente(cliente_id)}


@app.post("/api/solicitudes/{solicitud_id}/cancelar")
async def api_cancelar_solicitud(solicitud_id: int):
    try:
        return db.cancelar_solicitud(solicitud_id)
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})


@app.post("/api/solicitudes/{solicitud_id}/cerrar")
async def api_cerrar_solicitud(solicitud_id: int):
    try:
        return db.cerrar_solicitud(solicitud_id)
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})


# ============================================================
# ENDPOINTS API - OFERTAS
# ============================================================

@app.post("/api/ofertas")
async def api_crear_oferta(
    solicitud_id: int = Form(...), proveedor_id: int = Form(...),
    mensaje: str = Form(...), precio: Optional[float] = Form(None),
):
    try:
        resultado = db.crear_oferta(solicitud_id, proveedor_id, mensaje, precio)
        return {"ok": True, "oferta": resultado.data}
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})


@app.get("/api/solicitudes/{solicitud_id}/ofertas")
async def api_listar_ofertas(solicitud_id: int):
    return {"ofertas": db.listar_ofertas_de_solicitud(solicitud_id)}


@app.get("/api/solicitudes/{solicitud_id}/ofertas-detalladas")
async def api_listar_ofertas_detalladas(solicitud_id: int):
    return {"ofertas": db.listar_ofertas_con_proveedor(solicitud_id)}


@app.post("/api/ofertas/{oferta_id}/aceptar")
async def api_aceptar_oferta(oferta_id: int):
    try:
        return db.aceptar_oferta(oferta_id)
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})


@app.post("/api/ofertas/{oferta_id}/cancelar-aceptacion")
async def api_cancelar_aceptacion(oferta_id: int):
    try:
        return db.cancelar_aceptacion(oferta_id)
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})


# ============================================================
# ENDPOINTS API - NOTIFICACIONES
# ============================================================

@app.get("/api/usuarios/{usuario_id}/notificaciones")
async def api_listar_notificaciones(usuario_id: int, solo_no_leidas: bool = False):
    return {"notificaciones": db.listar_notificaciones(usuario_id, solo_no_leidas)}


@app.get("/api/usuarios/{usuario_id}/notificaciones-detalladas")
async def api_listar_notificaciones_detalladas(usuario_id: int, solo_no_leidas: bool = False):
    return {"notificaciones": db.listar_notificaciones_detalladas(usuario_id, solo_no_leidas)}


@app.get("/api/usuarios/{usuario_id}/notificaciones/contar")
async def api_contar_notificaciones(usuario_id: int):
    return {"no_leidas": db.contar_notificaciones_no_leidas(usuario_id)}


@app.post("/api/notificaciones/{notificacion_id}/leer")
async def api_marcar_leida(notificacion_id: int):
    try:
        return db.marcar_notificacion_leida(notificacion_id)
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})


@app.post("/api/usuarios/{usuario_id}/notificaciones/leer-todas")
async def api_marcar_todas_leidas(usuario_id: int):
    try:
        return db.marcar_todas_leidas(usuario_id)
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})


# ============================================================
# ENDPOINTS API - PROVEEDOR CATEGORIAS
# ============================================================

@app.get("/api/proveedores/{proveedor_id}/categorias")
async def api_categorias_de_proveedor(proveedor_id: int):
    return {"categorias": db.listar_categorias_de_proveedor(proveedor_id)}


@app.post("/api/proveedores/{proveedor_id}/categorias")
async def api_agregar_categoria_proveedor(
    proveedor_id: int,
    categoria_id: int = Form(...),
):
    try:
        return db.agregar_categoria_a_proveedor(proveedor_id, categoria_id)
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})


@app.delete("/api/proveedores/{proveedor_id}/categorias/{categoria_id}")
async def api_quitar_categoria_proveedor(proveedor_id: int, categoria_id: int):
    try:
        return db.quitar_categoria_de_proveedor(proveedor_id, categoria_id)
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})


# ============================================================
# EJECUCION DIRECTA
# ============================================================

if __name__ == "__main__":
    import uvicorn
    print("\n=================================================")
    print("  Servidor QuienLoTiene corriendo")
    print("  Abre: http://localhost:8000")
    print("=================================================\n")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)