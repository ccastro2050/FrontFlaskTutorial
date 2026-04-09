"""
email_service.py - Servicio de email via SMTP.

Este servicio se usa para enviar correos electronicos, especificamente
para la recuperacion de contrasena (enviar contrasena temporal).

COMO FUNCIONA:
==============
1. El usuario olvida su contrasena y va a /recuperar-contrasena
2. El sistema genera una contrasena temporal aleatoria
3. Este servicio envia un correo con la temporal al usuario
4. El usuario usa la temporal para entrar y luego crea una nueva

CONFIGURACION SMTP (en config.py):
===================================
Para que el envio de correos funcione, hay que configurar un servidor SMTP.
Ejemplo con Gmail:
  SMTP_HOST = "smtp.gmail.com"
  SMTP_PORT = 587
  SMTP_USER = "tucuenta@gmail.com"
  SMTP_PASS = "xxxx xxxx xxxx xxxx"   <-- App Password, NO la contrasena normal
  SMTP_FROM = "tucuenta@gmail.com"

NOTA: Gmail requiere una "App Password" (contrasena de aplicacion).
Para obtenerla: Google Account > Security > 2-Step Verification > App Passwords.
La contrasena normal de Gmail NO funciona.

Si SMTP no esta configurado, el sistema cambia la contrasena pero
no puede enviar el correo (avisa al usuario con un warning).
"""

import smtplib
# dns.resolver es opcional - se usa para validar que el dominio del email existe.
# Si no esta instalado (pip install dnspython), se omite la validacion.
try:
    import dns.resolver
    HAS_DNS = True
except ImportError:
    HAS_DNS = False
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM


def validar_email_dominio(email):
    """
    Verifica que el dominio del email tenga servidor de correo (registro MX).

    Ejemplo: para "juan@empresa.com", verifica que "empresa.com" tenga
    un servidor de correo configurado.

    Esto evita enviar correos a dominios inexistentes (ahorra tiempo).
    Si dnspython no esta instalado, se omite la validacion.
    """
    if not HAS_DNS:
        return True, "dns.resolver no disponible, se omite validacion."
    try:
        dominio = email.split("@")[-1]
        registros = dns.resolver.resolve(dominio, "MX")
        if registros:
            return True, "Dominio valido."
        return False, f"El dominio \"{dominio}\" no tiene servidor de correo."
    except Exception:
        return True, "No se pudo verificar el dominio."


def enviar_correo(destinatario, asunto, cuerpo_html):
    """
    Envia un correo electronico via SMTP.

    Parametros:
      - destinatario: email del receptor (ej: "juan@mail.com")
      - asunto: titulo del correo
      - cuerpo_html: contenido del correo en formato HTML

    El proceso SMTP:
      1. Conectarse al servidor SMTP (ej: smtp.gmail.com:587)
      2. Iniciar encriptacion TLS (conexion segura)
      3. Autenticarse con usuario y contrasena SMTP
      4. Enviar el mensaje
      5. Cerrar la conexion

    Retorna:
      (True, "Correo enviado.") si se envio correctamente
      (False, "mensaje de error") si algo fallo
    """
    try:
        # Verificar que SMTP este configurado
        if not SMTP_USER or not SMTP_PASS:
            return False, "SMTP no configurado (ver config.py)."

        # Construir el mensaje de correo
        msg = MIMEMultipart("alternative")   # Tipo "alternative" permite HTML
        msg["From"] = SMTP_FROM              # Remitente
        msg["To"] = destinatario             # Destinatario
        msg["Subject"] = asunto              # Asunto
        msg.attach(MIMEText(cuerpo_html, "html", "utf-8"))  # Cuerpo en HTML

        # Enviar via SMTP
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()                              # Activar encriptacion TLS
            server.login(SMTP_USER, SMTP_PASS)             # Autenticarse
            server.sendmail(SMTP_FROM, destinatario, msg.as_string())  # Enviar

        return True, "Correo enviado."
    except Exception as ex:
        return False, str(ex)


def enviar_contrasena_temporal(destinatario, contrasena_temporal):
    """
    Envia un correo con la contrasena temporal al usuario.

    El correo tiene un diseno HTML profesional con:
      - Header azul con titulo "Recuperacion de Contrasena"
      - La contrasena temporal grande y visible
      - Aviso de que debe cambiarla al ingresar

    Parametros:
      - destinatario: email del usuario
      - contrasena_temporal: la contrasena generada aleatoriamente (ej: "Ak7xPm2q")
    """
    asunto = "Recuperacion de contrasena"
    cuerpo = f"""
    <html><body style="font-family:Arial,sans-serif;color:#333;max-width:600px;margin:0 auto">
        <div style="background:#0d6efd;color:white;padding:20px;text-align:center;border-radius:8px 8px 0 0">
            <h2 style="margin:0">Recuperacion de Contrasena</h2>
        </div>
        <div style="padding:30px;background:#f8f9fa;border:1px solid #dee2e6;border-top:none;border-radius:0 0 8px 8px">
            <p>Su nueva contrasena temporal es:</p>
            <div style="background:white;border:2px solid #0d6efd;border-radius:8px;padding:15px;text-align:center;margin:20px 0">
                <span style="font-size:24px;font-weight:bold;letter-spacing:3px;color:#0d6efd">{contrasena_temporal}</span>
            </div>
            <p><strong>Al ingresar, el sistema le pedira crear una nueva contrasena.</strong></p>
        </div>
    </body></html>"""
    return enviar_correo(destinatario, asunto, cuerpo)
