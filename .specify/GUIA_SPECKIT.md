# Guia Completa: GitHub Spec-Kit en FrontFlaskTutorial

> Este documento explica paso a paso como se instalo y uso GitHub Spec-Kit
> en este proyecto. Sirve como referencia para replicar en otros proyectos
> y como material para el curso de Diseno de Software.

---

## 1. Que es GitHub Spec-Kit

GitHub Spec-Kit es el toolkit oficial de GitHub para **Spec-Driven Development (SDD)**.
Es una herramienta de linea de comandos que estandariza como se documenta y planifica
un proyecto antes de escribir codigo.

> "Lo mas importante del SDD es que la documentacion es un entregable que se versiona,
> y el codigo es el resultado de esta documentacion."

### Referencias

- Repositorio oficial: [github.com/github/spec-kit](https://github.com/github/spec-kit)
- Documento tecnico: [spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- Blog Microsoft: [Diving Into SDD With Spec Kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)
- Video conceptual: [La forma CORRECTA de programar con IA en 2026: SDD](https://youtu.be/p2WA672HrdI)
- Video tutorial: [GitHub Spec Kit - Tutorial completo con ejemplo](https://youtu.be/QzSCmSFKvko)

---

## 2. Las 5 fases del SDD

| # | Fase | Comando | Que genera | Descripcion |
|---|------|---------|-----------|-------------|
| 1 | **Constitution** | `/speckit-constitution` | `constitution.md` | Reglas no negociables: tecnologias, convenciones, prohibiciones |
| 2 | **Specify** | `/speckit-specify` | `spec.md` | Que se construye: historias de usuario con Given/When/Then |
| 3 | **Plan** | `/speckit-plan` | `plan.md` | Como se construye: arquitectura, componentes, endpoints |
| 4 | **Tasks** | `/speckit-tasks` | `tasks.md` | Lista de tareas ejecutables con dependencias |
| 5 | **Implement** | `/speckit-implement` | Codigo fuente | La IA ejecuta las tareas y genera el codigo |

### Comandos opcionales

| Comando | Cuando usarlo |
|---------|--------------|
| `/speckit-clarify` | Antes de plan: resolver ambiguedades |
| `/speckit-analyze` | Despues de tasks: validar consistencia entre spec, plan y tasks |
| `/speckit-checklist` | Despues de plan: generar checklist de calidad |

---

## 3. Instalacion paso a paso

### 3.1 Prerrequisitos

| Herramienta | Como instalar | Para que |
|------------|--------------|----------|
| Python 3.11+ | [python.org](https://www.python.org/downloads/) | Runtime del CLI |
| Git | [git-scm.com](https://git-scm.com/) | Control de versiones |
| uv | `pip install uv` | Gestor de paquetes (recomendado por GitHub) |

### 3.2 Instalar uv

```powershell
pip install uv
uv --version   # Verificar: debe mostrar version (ej: 0.11.7)
```

### 3.3 Verificar que specify funciona

```powershell
# En Windows necesita PYTHONIOENCODING por los emojis del banner
$env:PYTHONIOENCODING = "utf-8"
uvx --from git+https://github.com/github/spec-kit.git specify version
```

Debe mostrar:
```
CLI Version    0.7.2.dev0
Python         3.14.0
Platform       Windows
```

### 3.4 Inicializar en un proyecto existente

```powershell
cd C:\ruta\a\tu\proyecto
$env:PYTHONIOENCODING = "utf-8"
uvx --from git+https://github.com/github/spec-kit.git specify init --here --integration claude
```

Opciones:
- `--here`: inicializar en el directorio actual (no crear subcarpeta)
- `--integration claude`: configurar para Claude Code
- Otras integraciones: `copilot`, `gemini`, `cursor`, `windsurf`

Si el directorio no esta vacio, pregunta confirmacion. Responder `y`.

### 3.5 Inicializar en un proyecto nuevo

```powershell
$env:PYTHONIOENCODING = "utf-8"
uvx --from git+https://github.com/github/spec-kit.git specify init MiProyecto --integration claude
cd MiProyecto
```

---

## 4. Que genera specify init

```
tu-proyecto/
├── .specify/                              <- Carpeta principal de Spec-Kit
│   ├── memory/
│   │   └── constitution.md               <- Plantilla constitucion (LLENAR)
│   ├── templates/
│   │   ├── constitution-template.md      <- Formato para constituciones
│   │   ├── spec-template.md              <- Formato para especificaciones
│   │   ├── plan-template.md              <- Formato para planes
│   │   ├── tasks-template.md             <- Formato para tareas
│   │   └── checklist-template.md         <- Formato para checklists
│   ├── scripts/powershell/               <- Scripts de automatizacion
│   ├── extensions/git/                   <- Extension para commits/branches
│   ├── integrations/claude/              <- Integracion con Claude Code
│   ├── workflows/speckit/                <- Workflow de Spec-Kit
│   ├── init-options.json                 <- Opciones usadas en init
│   └── integration.json                  <- Integracion activa
│
└── .claude/skills/                       <- Skills de Claude Code
    ├── speckit-constitution/SKILL.md
    ├── speckit-specify/SKILL.md
    ├── speckit-plan/SKILL.md
    ├── speckit-tasks/SKILL.md
    ├── speckit-implement/SKILL.md
    ├── speckit-clarify/SKILL.md
    ├── speckit-analyze/SKILL.md
    └── speckit-checklist/SKILL.md
```

**IMPORTANTE**: `specify init` genera PLANTILLAS vacias con placeholders.
Los archivos se llenan ejecutando los slash commands o manualmente.

---

## 5. Como usar las 5 fases (con ejemplo)

### Fase 1: Constitution

Ejecutar `/speckit-constitution` en Claude Code (o llenar manualmente).

Escribir los principios del proyecto:
```
Proyecto Flask + Jinja2 + Bootstrap 5 que consume API REST en C#.
Principios: API-First, SOLID, ACID, seguridad en 3 capas (BCrypt, JWT, sesion).
Prohibido: ORM, push directo a main, hardcodear URLs.
```

Resultado: `.specify/memory/constitution.md` con los principios formalizados.

### Fase 2: Specify

Ejecutar `/speckit-specify` describiendo la feature:
```
Feature: Login y control de acceso.
El usuario se autentica con email+contrasena (BCrypt via API).
Se cargan roles y rutas permitidas. El middleware verifica en cada request.
```

Resultado: `.specify/specs/{feature}/spec.md` con User Stories y Given/When/Then.

### Fase 3: Plan

Ejecutar `/speckit-plan`. La IA lee constitution + spec y genera el plan tecnico:
- Arquitectura
- Componentes (archivos a crear/modificar)
- Endpoints de la API
- Decisiones tecnicas con justificacion

Resultado: `.specify/specs/{feature}/plan.md`

### Fase 4: Tasks

Ejecutar `/speckit-tasks`. La IA lee spec + plan y genera tareas ejecutables:
- Organizadas por User Story
- Con dependencias entre tareas
- Marcador `[P]` para tareas paralelizables
- Rutas de archivos especificas

Resultado: `.specify/specs/{feature}/tasks.md`

### Fase 5: Implement

Ejecutar `/speckit-implement`. La IA ejecuta cada tarea del tasks.md:
- Crea archivos
- Modifica existentes
- Valida contra la constitucion

Resultado: Codigo fuente en el proyecto.

---

## 6. Estructura de specs por feature

Cada feature tiene su propia carpeta con 3 archivos:

```
.specify/specs/
├── 001-proyecto-base/
│   ├── spec.md          <- Que: crear proyecto Flask, config, git
│   ├── plan.md          <- Como: estructura carpetas, app.py, config.py
│   └── tasks.md         <- Tareas: crear archivos, git init, push
│
├── 006-crud-producto/
│   ├── spec.md          <- Que: CRUD de producto con formulario
│   ├── plan.md          <- Como: Blueprint, template, ApiService
│   └── tasks.md         <- Tareas: crear route, template, registrar
│
├── 010-factura-maestro-detalle/
│   ├── spec.md          <- Que: factura con cabecera + detalle
│   ├── plan.md          <- Como: JS dinamico, selects FK, calculo total
│   └── tasks.md         <- Tareas: route, template, JS
│
└── 012-login-y-control-acceso/
    ├── spec.md          <- Que: login, roles, rutas, JWT, BCrypt
    ├── plan.md          <- Como: AuthService, middleware, ConsultasController
    └── tasks.md         <- Tareas: servicios, rutas, templates, middleware
```

---

## 7. Flujo completo resumido

```
1. pip install uv
2. uvx ... specify init --here --integration claude
3. /speckit-constitution  ->  .specify/memory/constitution.md
4. /speckit-specify       ->  .specify/specs/{feature}/spec.md
5. /speckit-plan          ->  .specify/specs/{feature}/plan.md
6. /speckit-tasks         ->  .specify/specs/{feature}/tasks.md
7. /speckit-implement     ->  Codigo fuente
8. (opcional) /speckit-analyze   ->  Validar consistencia
9. (opcional) /speckit-checklist ->  Checklist de calidad
```

---

## 8. Tips y buenas practicas

### Del video [GitHub Spec Kit - Tutorial](https://youtu.be/QzSCmSFKvko):

> "Entre mas uses este flujo, mas te daras cuenta de lo que tienes que
> especificar en los comandos."

- **Constitution primero**: es lo que la IA lee SIEMPRE antes de generar codigo
- **Ser especifico en specify**: no decir "haz un CRUD", decir "CRUD de producto con campos codigo, nombre, precio, con select FK para categoria"
- **Revisar el plan**: no aceptar a ciegas, leer y validar antes de tasks
- **Agregar diagramas Mermaid**: ER, secuencia, clases (Spec-Kit no los incluye por defecto)

### De la experiencia en este proyecto:

- La constitucion debe incluir **SOLID, ACID, patrones de diseno** (no solo stack)
- Las specs deben tener **Given/When/Then** (criterios verificables)
- El plan debe tener **diagramas de secuencia** (la IA entiende mejor el flujo)
- Las tasks deben marcar `[P]` lo que se puede **paralelizar** (trabajo en equipo)
- Cada feature se versiona junto con el codigo (git add .specify/)

---

## 9. Comparacion: sin SDD vs con SDD

| Aspecto | Sin SDD | Con SDD (Spec-Kit) |
|---------|---------|-------------------|
| Planificacion | "Hazme un login" en el chat | Constitution + spec + plan + tasks |
| La IA inventa | Nombres, arquitectura, patrones | Sigue la constitucion |
| Retrabajo | 40-60% | 10-15% |
| Documentacion | No existe o esta desactualizada | ES el entregable principal |
| Trabajo en equipo | "Yo hice esto, tu haz lo otro" | Tasks con [P] y dependencias |
| Validacion | "A ver si funciona" | Given/When/Then verificables |

---

## 10. Archivos de este proyecto

### Documentacion SDD manual (sdd/)

Creada ANTES de instalar Spec-Kit. Contenido educativo extenso:

| Archivo | Lineas | Contenido |
|---------|--------|-----------|
| sdd/00_indice.md | 109 | Que es SDD, fases, referencias |
| sdd/01_constitucion.md | 322 | SOLID, ACID, patrones, arquitectura 3 capas |
| sdd/02_especificacion.md | 244 | Modelo ER, normalizacion, cardinalidad |
| sdd/03_clarificacion.md | 131 | Preguntas resueltas, ACID vs BASE |
| sdd/04_plan.md | 510 | 5 diagramas secuencia + diagrama clases (Mermaid) |
| sdd/05_tareas.md | 221 | Tareas por historia con [P] |
| sdd/06_specify_cli.md | 320 | Este proceso de instalacion |
| sdd/data-model.md | 224 | SQL completo PostgreSQL + SqlServer |

### Documentacion Spec-Kit oficial (.specify/)

Creada por `specify init` y llenada con datos reales:

| Archivo | Fase | Contenido |
|---------|------|-----------|
| .specify/memory/constitution.md | 1 | 6 principios, stack, convenciones, restricciones |
| .specify/specs/001-proyecto-base/spec.md | 2 | Feature: crear proyecto Flask |
| .specify/specs/001-proyecto-base/plan.md | 3 | Estructura carpetas, app.py |
| .specify/specs/001-proyecto-base/tasks.md | 4 | Tareas: crear archivos, git |
| ... (8 features mas) | | |
| .specify/specs/012-login/spec.md | 2 | 5 User Stories con Given/When/Then |
| .specify/specs/012-login/plan.md | 3 | Componentes, endpoints, seguridad |
| .specify/specs/012-login/tasks.md | 4 | Tareas detalladas, todas completadas |

**Ambas carpetas coexisten y se complementan. Ninguna se borra.**
