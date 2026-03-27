# Paso 3 — Crear el Proyecto y Configurar GitHub con 3 Cuentas

---

## Parte A: Crear el proyecto Flask

### 1. Abrir terminal en la carpeta de proyectos

```powershell
cd C:\Users\TU_USUARIO\Desktop\proyectoscsharp
```

### 2. Crear la carpeta del proyecto

```bash
mkdir FrontFlaskTutorial
cd FrontFlaskTutorial
```

### 3. Crear el entorno virtual

```powershell
python -m venv venv       # crea carpeta venv/ con una copia aislada de Python
```

### 4. Activar el entorno virtual

```powershell
venv\Scripts\activate     # activa el entorno (aparece "(venv)" al inicio de la línea)
```

**¿Qué es activar el venv?** Desde este momento, `pip install` instala paquetes solo dentro de esta carpeta, sin afectar el Python del sistema. Cada vez que se abre una terminal nueva, hay que volver a activar con `venv\Scripts\activate`.

### 5. Instalar dependencias

```powershell
pip install flask requests    # instala Flask (servidor web) y requests (peticiones HTTP)
```

### 6. Crear el archivo de dependencias

```powershell
pip freeze > requirements.txt   # guarda la lista de paquetes instalados con sus versiones
```

Este archivo permite que cualquier persona que clone el proyecto pueda instalar las mismas dependencias con `pip install -r requirements.txt`.

### 7. Crear la estructura de carpetas

```powershell
mkdir routes, services, templates, static, scripts_bds          # carpetas principales
mkdir templates\layout, templates\components, templates\pages, static\css   # subcarpetas
```

### 8. Crear los archivos iniciales

Crear los archivos `__init__.py` (vacíos, necesarios para que Python reconozca las carpetas como paquetes):

```powershell
New-Item routes\__init__.py       # init del paquete routes
New-Item services\__init__.py     # init del paquete services
```

### 9. Crear `config.py`

Crear el archivo `config.py` en la raíz del proyecto con este contenido:

```python
"""
config.py - Configuracion centralizada de la aplicacion Flask.
"""

# URL base de la API REST que consume este frontend.
# La API generica en C# corre en el puerto 5035.
API_BASE_URL = "http://localhost:5035"

# Clave secreta para el manejo de sesiones y mensajes flash.
SECRET_KEY = "clave-secreta-flask-frontend-2024"
```

### 10. Crear `app.py`

Crear el archivo `app.py` en la raíz del proyecto:

```python
"""
app.py - Punto de entrada de la aplicacion Flask.
"""

from flask import Flask
from config import SECRET_KEY

# Crear la aplicacion Flask
app = Flask(__name__)
app.secret_key = SECRET_KEY

# (Aqui se registraran los Blueprints en pasos posteriores)

if __name__ == '__main__':
    app.run(debug=True, port=5300)
```

### 11. Verificar que funciona

```bash
python app.py
```

Debe mostrar algo como:
```
 * Running on http://127.0.0.1:5100
```

Abrir en el navegador: `http://localhost:5300`. Mostrará un error 404 porque aún no hay rutas — eso es correcto. Cerrar con `Ctrl+C`.

### 12. Crear `.gitignore`

Crear el archivo `.gitignore` en la raíz del proyecto:

```
# Entorno virtual - cada persona crea el suyo
venv/

# Cache de Python
__pycache__/
*.pyc
*.pyo

# Archivos del IDE
.vscode/
.idea/
*.swp

# Variables de entorno
.env

# Archivos del sistema
.DS_Store
Thumbs.db
```

**Importante:** `venv/` **NO se sube a GitHub**. Cada persona que clona el proyecto crea su propio entorno virtual e instala las dependencias con `pip install -r requirements.txt`.

---

## Parte B: Flujo de trabajo con Git y GitHub

```
┌──────────────────────────────────────────────────────────────────────────┐
│  main  ○──○──○──○──○──○──○──○──○──○──○──○───────────────────→           │
│            ├── crud-producto ●──● ─ merge ─┘  (Estudiante 1)            │
│            │         ├── crud-empresa ●──● ─ merge ─┘  (Estudiante 1)   │
│            │                                                             │
│            ├── crud-persona ●──● ─ merge ─┘  (Estudiante 2)            │
│            │         ├── crud-cliente ●──● ─ merge ─┘  (Estudiante 2)   │
│            │                                                             │
│            └── crud-usuario ●──● ─ merge ─┘  (Estudiante 3)            │
│                      └── crud-rol ●──● ─ merge ─┘  (Estudiante 3)      │
│                                                                          │
│  Flujo: push a rama → Est.1 hace git fetch + git merge desde terminal   │
└──────────────────────────────────────────────────────────────────────────┘
```

Nadie trabaja directamente en `main`. Cada tarea se hace en su propia rama. Cuando se termina, Estudiante 1 fusiona desde la terminal con `git merge`.

| Cuenta | Rol | Ramas | Permisos |
|--------|-----|-------|----------|
| **Estudiante 1** | Administrador del repositorio | Una rama por tarea (ej: `crud-producto`, `crud-empresa`) | Owner — crea el repo, invita, trabaja en sus ramas, fusiona ramas desde la terminal a main |
| **Estudiante 2** | Colaborador | Una rama por tarea (ej: `crud-persona`, `crud-cliente`) | Write — trabaja en sus ramas, sube con git push |
| **Estudiante 3** | Colaborador | Una rama por tarea (ej: `crud-usuario`, `crud-rol`) | Write — trabaja en sus ramas, sube con git push |

---

## Parte C: Lo que hace Estudiante 1 (Administrador)

### C1. Inicializar Git en el proyecto

Desde la carpeta `FrontFlaskTutorial`:

```bash
git init                                    # inicializa el repositorio git
git add .                                   # agrega todos los archivos al staging
git commit -m "Proyecto Flask inicial"      # guarda el primer snapshot del proyecto
```

### C2. Crear el repositorio en GitHub

1. Ir a https://github.com/new
2. Nombre: `FrontFlaskTutorial`
3. Visibilidad: **Private** (solo los colaboradores pueden ver el código)
4. **No** marcar ninguna casilla (no README, no .gitignore, no license)
5. Clic en **Create repository**

**¿Por qué Private?** En un proyecto académico o de empresa, el código no debe ser público. Solo los miembros del equipo (y el profesor) deben tener acceso.

### C3. Subir el proyecto

```bash
git remote add origin https://github.com/TU_USUARIO/FrontFlaskTutorial.git   # conecta el repo local con GitHub
git branch -M main                   # renombra la rama principal a "main"
git push -u origin main              # sube el código a GitHub por primera vez
```

### C4. Invitar a Estudiante 2 y Estudiante 3

1. Ir al repositorio en GitHub: `https://github.com/TU_USUARIO/FrontFlaskTutorial`
2. Clic en **Settings** (pestaña superior derecha)
3. En el menú izquierdo: **Collaborators** (dentro de "Access")
4. Clic en **Add people**
5. Escribir el nombre de usuario de GitHub de **Estudiante 2** → Clic en **Add**
6. Repetir para **Estudiante 3**

Los estudiantes 2 y 3 recibirán un correo con la invitación. Deben aceptarla.

### C5. Agregar el .gitignore y remover archivos innecesarios

Si por error se subió `venv/` o `__pycache__/`:

```bash
git rm -r --cached venv/              # remueve venv del tracking de git (no borra los archivos)
git rm -r --cached __pycache__/       # remueve __pycache__ del tracking
git add .gitignore
git commit -m "Agregar .gitignore y remover venv del repositorio"
git push
```

---

## Parte D: Lo que hacen Estudiante 2 y Estudiante 3

### D1. Aceptar la invitación

1. Iniciar sesión en GitHub con su cuenta
2. Ir a https://github.com/notifications
3. Aparece: **"Invitation to join [usuario]/FrontFlaskTutorial"**
4. Clic en esa notificación → **Accept invitation**

### D2. Clonar el repositorio

```bash
cd C:\Users\TU_USUARIO\Desktop\proyectoscsharp
git clone https://github.com/USUARIO_EST1/FrontFlaskTutorial.git    # descarga el proyecto
cd FrontFlaskTutorial
```

### D3. Crear el entorno virtual e instalar dependencias

Cada estudiante debe crear su propio `venv` (porque no se sube a GitHub):

```bash
python -m venv venv                   # crear entorno virtual
venv\Scripts\activate                 # activar
pip install -r requirements.txt       # instalar las mismas dependencias que Estudiante 1
```

### D4. Verificar que funciona

```bash
python app.py                         # debe arrancar en http://localhost:5300
```

### D5. Crear su rama de trabajo

**Estudiante 2** (si le toca CRUD Persona):
```bash
git checkout -b crud-persona          # crea rama y cambia a ella
git push -u origin crud-persona       # sube la rama a GitHub
```

**Estudiante 3** (si le toca CRUD Usuario):
```bash
git checkout -b crud-usuario
git push -u origin crud-usuario
```

---

## Parte E: Proceso de merge desde la terminal

### E1. Estudiante termina su tarea y sube los cambios

```bash
git add .                                          # agrega archivos modificados
git commit -m "Agregar ruta y template CRUD Persona"  # guarda cambios
git push origin crud-persona                       # sube a GitHub
```

### E2. Estudiante 1 fusiona desde la terminal

Estudiante 1 (administrador) descarga la rama del compañero y la fusiona en main:

```bash
git checkout main                                  # cambiar a la rama principal
git fetch origin                                   # descargar todas las ramas remotas
git merge origin/crud-persona                      # fusionar la rama del compañero en main
git push origin main                               # subir main actualizado a GitHub
```

Si hay conflictos, resolverlos en el editor, luego:

```bash
git add .                                          # marcar los conflictos como resueltos
git commit -m "Resolver conflictos de crud-persona"  # guardar la resolución
git push origin main                               # subir main actualizado
```

### E3. Eliminar la rama (opcional)

Una vez fusionada, la rama ya no es necesaria:

```bash
git branch -d crud-persona                         # eliminar rama local
git push origin --delete crud-persona              # eliminar rama remota
```

### E4. Todos actualizan main

Después de cada merge, los demás estudiantes deben actualizar:

```bash
git checkout main                     # volver a la rama principal
git pull                              # descargar los cambios mergeados
```

---

## Parte F: Resumen de comandos

| Comando | Qué hace |
|---------|----------|
| `git init` | Inicializa un repositorio Git |
| `git add .` | Agrega todos los archivos al staging |
| `git commit -m "msg"` | Guarda los cambios con un mensaje |
| `git push` | Sube los cambios a GitHub |
| `git pull` | Descarga y aplica cambios de GitHub |
| `git clone <url>` | Descarga un repositorio completo |
| `git checkout -b <rama>` | Crea una rama nueva y cambia a ella |
| `git checkout main` | Cambia a la rama main |
| `git branch` | Lista las ramas locales |
| `git status` | Muestra qué archivos cambiaron |
| `git fetch origin` | Descarga cambios de GitHub sin aplicarlos |
| `git merge origin/<rama>` | Fusiona una rama remota en la rama actual |
| `git push origin --delete <rama>` | Elimina una rama remota en GitHub |
| `git remote add origin <url>` | Conecta el repo local con GitHub |

---

> **Siguiente paso:** Paso 4 — Conexión a la API y ApiService.
