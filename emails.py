"""
Sistema de correos electronicos para QuienLoTiene.
Usa Resend con plantillas HTML bonitas y profesionales.
"""

import os
from dotenv import load_dotenv
import resend

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

REMITENTE = "QuienLoTiene <no-reply@envios.quienlotiene.net>"
SITIO_WEB = "https://www.quienlotiene.net"


def _plantilla_base(titulo: str, contenido_html: str) -> str:
    """Envuelve el contenido en la plantilla base con header y footer de QuienLoTiene."""
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
</head>
<body style="margin:0; padding:0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color:#f3f4f6; color:#1f2937;">
    
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#f3f4f6; padding: 30px 10px;">
        <tr>
            <td align="center">
                
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="max-width:600px; background-color:#ffffff; border-radius:12px; overflow:hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    
                    <!-- HEADER AZUL -->
                    <tr>
                        <td style="background-color:#2563eb; padding: 30px 40px; text-align:center;">
                            <h1 style="margin:0; color:#ffffff; font-size:28px; font-weight:bold;">QuienLoTiene</h1>
                            <p style="margin: 8px 0 0 0; color:#dbeafe; font-size:14px;">Conectando personas con lo que necesitan</p>
                        </td>
                    </tr>
                    
                    <!-- CONTENIDO -->
                    <tr>
                        <td style="padding: 40px;">
                            {contenido_html}
                        </td>
                    </tr>
                    
                    <!-- FOOTER -->
                    <tr>
                        <td style="background-color:#f9fafb; padding: 24px 40px; text-align:center; border-top: 1px solid #e5e7eb;">
                            <p style="margin:0; color:#6b7280; font-size:13px;">
                                Este correo fue enviado por QuienLoTiene.
                            </p>
                            <p style="margin:8px 0 0 0; color:#6b7280; font-size:13px;">
                                <a href="{SITIO_WEB}" style="color:#2563eb; text-decoration:none; font-weight:bold;">{SITIO_WEB}</a>
                            </p>
                            <p style="margin:16px 0 0 0; color:#9ca3af; font-size:11px;">
                                Si no te registraste en QuienLoTiene, puedes ignorar este mensaje.
                            </p>
                        </td>
                    </tr>
                    
                </table>
                
            </td>
        </tr>
    </table>
    
</body>
</html>
"""


def _boton(texto: str, url: str) -> str:
    """Genera un boton HTML azul estilizado."""
    return f"""
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin: 24px auto;">
            <tr>
                <td style="background-color:#2563eb; border-radius:8px;">
                    <a href="{url}" style="display:inline-block; padding: 14px 32px; color:#ffffff; text-decoration:none; font-weight:bold; font-size:15px;">{texto}</a>
                </td>
            </tr>
        </table>
    """


def enviar_bienvenida(email: str, nombre: str, rol: str = "cliente") -> dict:
    """
    Envia el correo de bienvenida a un usuario recien registrado.
    Devuelve {"ok": True, "id": "..."} o {"ok": False, "error": "..."}
    """
    try:
        if not resend.api_key:
            return {"ok": False, "error": "Falta RESEND_API_KEY en .env"}

        primer_nombre = nombre.split()[0] if nombre else "amigo"
        
        # Contenido personalizado segun rol
        if rol == "proveedor":
            mensaje_rol = """
                <p style="font-size:15px; line-height:1.6; color:#374151;">
                    Como <strong>proveedor</strong>, tu cuenta está lista para que ofrezcas 
                    productos o servicios a las personas que los necesiten.
                </p>
                <p style="font-size:15px; line-height:1.6; color:#374151;">
                    Sigue estos pasos:
                </p>
                <ol style="font-size:15px; line-height:1.6; color:#374151; padding-left:20px;">
                    <li>Configura las <strong>categorías</strong> en las que trabajas</li>
                    <li>Recibirás <strong>notificaciones</strong> cuando alguien busque algo de tu rubro</li>
                    <li>Envía ofertas y cierra tratos por WhatsApp</li>
                </ol>
            """
            cta = _boton("Ir a mi panel de proveedor", f"{SITIO_WEB}/proveedor")
        else:
            mensaje_rol = """
                <p style="font-size:15px; line-height:1.6; color:#374151;">
                    Como <strong>cliente</strong>, ya puedes publicar lo que necesitas 
                    y los proveedores te contactarán directamente.
                </p>
                <p style="font-size:15px; line-height:1.6; color:#374151;">
                    ¿Buscas algo específico? Publícalo y olvídate de perder tiempo 
                    llamando uno por uno a quienes no lo tienen.
                </p>
            """
            cta = _boton("Publicar mi primera solicitud", f"{SITIO_WEB}/")

        contenido = f"""
            <h2 style="margin: 0 0 16px 0; color:#111827; font-size:24px;">¡Bienvenido, {primer_nombre}! 🎉</h2>
            
            <p style="font-size:15px; line-height:1.6; color:#374151;">
                Tu cuenta en <strong>QuienLoTiene</strong> ha sido creada exitosamente.
            </p>
            
            {mensaje_rol}
            
            {cta}
            
            <div style="background-color:#f0f9ff; border-left: 4px solid #2563eb; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin:0; font-size:13px; color:#1e40af;">
                    <strong>💡 Consejo:</strong> Confirma tu correo electrónico haciendo clic 
                    en el enlace que te enviamos en el mensaje anterior. Así activas tu cuenta por completo.
                </p>
            </div>
            
            <p style="font-size:14px; line-height:1.6; color:#6b7280; margin-top:24px;">
                Si tienes alguna duda, respóndenos a este correo. Estamos aquí para ayudarte.
            </p>
            
            <p style="font-size:14px; color:#6b7280;">
                — El equipo de QuienLoTiene
            </p>
        """

        html = _plantilla_base("Bienvenido a QuienLoTiene", contenido)

        params = {
            "from": REMITENTE,
            "to": [email],
            "subject": f"¡Bienvenido a QuienLoTiene, {primer_nombre}!",
            "html": html,
        }

        resultado = resend.Emails.send(params)
        return {"ok": True, "id": resultado.get("id", "N/A")}

    except Exception as e:
        return {"ok": False, "error": str(e)}