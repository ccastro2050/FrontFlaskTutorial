# Paso 2 — Herramientas

Antes de escribir código, estas son las herramientas que se necesitan instaladas en Windows.

---

## 1. Python 3

**Qué es:** Lenguaje de programación. Flask corre sobre Python.

**Qué hace en este proyecto:**
- Ejecutar el servidor Flask (`python app.py`)
- Crear entornos virtuales (`python -m venv venv`)
- Instalar librerías (`pip install flask requests`)

**Verificar instalación:**
```bash
python --version       # Debe mostrar Python 3.x
pip --version          # Debe mostrar pip 2x.x
```

**Descargar:** https://www.python.org/downloads/

Durante la instalación, **marcar la casilla "Add Python to PATH"**. Sin esto, los comandos `python` y `pip` no funcionan desde la terminal.

---

## 2. Git

**Qué es:** Sistema de control de versiones.

**Qué hace en este proyecto:**
- Guardar el historial de cambios (`git commit`)
- Crear ramas para trabajar sin afectar el código principal (`git branch`)
- Subir el proyecto a GitHub (`git push`)
- Descargar proyectos existentes (`git clone`)

**Comandos que se van a usar:**
```bash
git init                    # Inicializar un repositorio nuevo
git add .                   # Preparar archivos para guardar
git commit -m "mensaje"     # Guardar cambios con descripción
git push                    # Subir cambios a GitHub
git clone <url>             # Descargar un repositorio
git status                  # Ver qué archivos cambiaron
git checkout -b <rama>      # Crear y cambiar a una rama nueva
git pull                    # Descargar y aplicar cambios de GitHub
git fetch origin            # Solo descargar cambios sin aplicar
git merge origin/main       # Aplicar cambios de main a la rama actual
```

**Descargar:** https://git-scm.com/download/win

---

## 3. Visual Studio Code

**Qué es:** Editor de código.

**Extensiones recomendadas:**
- **Python** (Microsoft) — soporte para Python, autocompletado, debug
- **Pylance** — análisis de código Python más avanzado
- **Jinja** — resaltado de sintaxis para templates Jinja2
- **GitLens** — ver quién modificó cada línea de código

**Descargar:** https://code.visualstudio.com/

---

## 4. Cuenta de GitHub

**Qué es:** Plataforma para alojar repositorios Git en la nube.

**Qué hace en este proyecto:**
- Almacenar el código del equipo
- Gestionar Pull Requests (revisión de código)
- Controlar quién puede modificar `main`

**Crear cuenta:** https://github.com

Cada estudiante necesita su propia cuenta.

---

## Verificación rápida

Abrir una terminal (PowerShell o CMD) y ejecutar:

```bash
python --version       # Python 3.x
pip --version          # pip 2x.x
git --version          # git version 2.x
code --version         # Visual Studio Code 1.x
```

Si alguno falla, instalar la herramienta correspondiente.

---

> **Siguiente paso:** Paso 3 — Crear el Proyecto y Configurar GitHub.
