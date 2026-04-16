# OpenSpec - Instalacion, Uso y Comparacion con Spec-Kit

> OpenSpec es el framework open source de [Fission AI](https://github.com/Fission-AI/OpenSpec)
> para Spec Driven Development (SDD). Con 30.000+ estrellas en GitHub, es compatible con
> 20+ agentes de IA (Claude Code, Cursor, Copilot, Gemini, OpenCode, etc.).
>
> A diferencia de Spec-Kit (GitHub) que es para proyectos nuevos (greenfield),
> OpenSpec esta disenado para proyectos existentes (brownfield) con el concepto
> de **delta specs** — cambios incrementales que no reescriben toda la spec.

---

## 1. Que es OpenSpec

OpenSpec convierte el SDD en un flujo de trabajo con herramientas reales.
No es una plantilla de Markdown — es una CLI que se instala con npm y se
integra con tu agente de IA.

### 4 principios de OpenSpec

| Principio | Que significa |
|-----------|-------------|
| **Fluido, no rigido** | No hay puertas de fase. Puedes volver atras cuando quieras |
| **Iterativo, no waterfall** | Aprende mientras construyes, refina sobre la marcha |
| **Facil, no complejo** | Configuracion minima, arranque en segundos |
| **Brownfield first** | Disenado para proyectos existentes, no solo para nuevos |

### 4 conceptos fundamentales

| Concepto | Que es | Donde vive |
|----------|--------|-----------|
| **Specs** | Fuente de verdad: como se comporta el sistema AHORA | `openspec/specs/{dominio}/spec.md` |
| **Changes** | Propuestas de cambio (carpeta autocontenida) | `openspec/changes/{nombre}/` |
| **Artefactos** | Documentos dentro de un change (proposal, design, tasks, delta specs) | Dentro de cada change |
| **Delta Specs** | Cambios incrementales a las specs (ADDED, MODIFIED, REMOVED) | `openspec/changes/{nombre}/specs/` |

### Referencias

- Repositorio: [github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
- Documentacion: [OpenSpec Getting Started](https://github.com/Fission-AI/OpenSpec)
- Guia detallada: [webreactiva.com/blog/openspec](https://www.webreactiva.com/blog/openspec)
- npm: [@fission-ai/openspec](https://www.npmjs.com/package/@fission-ai/openspec)

---

## 2. Instalacion paso a paso

### 2.1 Prerrequisitos

| Herramienta | Version minima | Como verificar |
|------------|---------------|----------------|
| Node.js | 20.19.0+ | `node --version` |
| npm | (incluido) | `npm --version` |
| Git | cualquiera | `git --version` |

### 2.2 Instalar OpenSpec

```powershell
npm install -g @fission-ai/openspec@latest
openspec --version   # Debe mostrar: 1.3.0 (o superior)
```

### 2.3 Inicializar en el proyecto

```powershell
cd C:\ruta\a\tu\proyecto
openspec init
```

El proceso pregunta que agente de IA usas. Seleccionar `Claude Code`.
OpenSpec crea los skills en `.claude/skills/` y los comandos en `.claude/commands/`.

### 2.4 Que genera openspec init

```
tu-proyecto/
├── openspec/
│   ├── specs/              <- Fuente de verdad (vacia al inicio)
│   └── changes/
│       └── archive/        <- Cambios archivados
│
└── .claude/
    ├── commands/opsx        <- Comandos OPSX
    └── skills/
        ├── openspec-propose/     <- /opsx:propose
        ├── openspec-apply-change/ <- /opsx:apply
        ├── openspec-archive-change/ <- /opsx:archive
        └── openspec-explore/     <- /opsx:explore
```

### 2.5 Desactivar telemetria (opcional)

```powershell
$env:OPENSPEC_TELEMETRY = "0"
```

---

## 3. Comandos de OpenSpec (OPSX)

### Comandos principales (perfil core)

| Comando | Que hace | Cuando usarlo |
|---------|----------|--------------|
| `/opsx:explore` | Modo exploratorio libre, sin crear artefactos | Cuando no tienes claro el enfoque |
| `/opsx:propose` | Crea un change con TODOS los artefactos (proposal, specs, design, tasks) | Inicio rapido, la mayoria de los casos |
| `/opsx:apply` | Implementa las tareas del change | Cuando el plan esta listo |
| `/opsx:archive` | Archiva el change y fusiona delta specs | Cuando todas las tareas estan completas |

### Comandos avanzados (perfil expandido)

| Comando | Que hace |
|---------|----------|
| `/opsx:new` | Crea solo la estructura del change (sin artefactos) |
| `/opsx:continue` | Genera el siguiente artefacto segun dependencias |
| `/opsx:ff` | Fast-forward: genera todos los artefactos de golpe |
| `/opsx:verify` | Valida implementacion contra specs |
| `/opsx:sync` | Fusiona delta specs sin archivar |
| `/opsx:bulk-archive` | Archiva varios changes a la vez |
| `/opsx:onboard` | Tutorial guiado con tu propio codigo |

> **Nota**: En Claude Code se usa dos puntos (`/opsx:propose`).
> En Cursor, OpenCode, Windsurf se usa guion (`/opsx-propose`).

---

## 4. Flujo completo con ejemplo

### Agregar una feature nueva al proyecto existente

```
Paso 1: Explorar la idea
> /opsx:explore
> "Necesito agregar exportacion CSV en la pagina de producto"
> La IA analiza el codigo existente y sugiere enfoques

Paso 2: Crear el change con artefactos
> /opsx:propose agregar-csv-producto
> Genera:
>   openspec/changes/agregar-csv-producto/
>   ├── proposal.md      <- Por que y que
>   ├── specs/            <- Delta specs (que cambia)
>   ├── design.md         <- Como (enfoque tecnico)
>   └── tasks.md          <- Checklist de implementacion

Paso 3: Revisar y ajustar
> Leer los artefactos, editar si falta algo

Paso 4: Implementar
> /opsx:apply
> La IA ejecuta tarea por tarea, marcando checkboxes

Paso 5: Archivar
> /opsx:archive
> Delta specs se fusionan con specs principales
> Change se mueve a openspec/changes/archive/
```

### Delta specs: el concepto clave

En vez de reescribir toda la spec, escribes SOLO lo que cambia:

```markdown
# Delta for Producto

## ADDED Requirements

### Requirement: CSV Export
El sistema DEBE permitir exportar la lista de productos a CSV.

## MODIFIED Requirements

### Requirement: Listar productos
El sistema DEBE mostrar un boton "Exportar CSV" en la tabla de productos.
(Previously: solo mostraba la tabla)
```

Al archivar, los deltas se fusionan: ADDED se agrega, MODIFIED reemplaza, REMOVED se elimina.

---

## 5. Estructura de archivos en este proyecto

Ahora el proyecto tiene **3 carpetas de documentacion SDD**:

```
FrontFlaskTutorial/
├── sdd/                    <- Documentacion manual (educativa, extensa)
│   ├── 00_indice.md
│   ├── 01_constitucion.md   (SOLID, ACID, patrones, 322 lineas)
│   ├── 02_especificacion.md (modelo ER, normalizacion, 244 lineas)
│   ├── 03_clarificacion.md  (preguntas resueltas, 131 lineas)
│   ├── 04_plan.md           (diagramas Mermaid, 510 lineas)
│   ├── 05_tareas.md         (por historia, 221 lineas)
│   ├── 06_specify_cli.md    (instalacion Spec-Kit)
│   ├── 07_openspec.md       (ESTE archivo)
│   └── data-model.md        (SQL completo, 224 lineas)
│
├── .specify/               <- Spec-Kit de GitHub (greenfield)
│   ├── memory/constitution.md
│   ├── specs/001-proyecto-base/{spec,plan,tasks}.md
│   ├── specs/004-api-service/{spec,plan,tasks}.md
│   ├── specs/005-layout-navegacion/{spec,plan,tasks}.md
│   ├── specs/006-crud-producto/{spec,plan,tasks}.md
│   ├── specs/007-crud-persona-usuario/{spec,plan,tasks}.md
│   ├── specs/008-crud-empresa-cliente-rol/{spec,plan,tasks}.md
│   ├── specs/009-crud-ruta-vendedor/{spec,plan,tasks}.md
│   ├── specs/010-factura-maestro-detalle/{spec,plan,tasks}.md
│   ├── specs/012-login-y-control-acceso/{spec,plan,tasks}.md
│   ├── templates/*.md
│   └── GUIA_SPECKIT.md
│
└── openspec/               <- OpenSpec de Fission AI (brownfield)
    ├── specs/               (se llenara con delta specs por dominio)
    └── changes/
        └── archive/         (changes completados)
```

---

## 6. Comparacion detallada: Spec-Kit vs OpenSpec

### Tabla comparativa general

| Aspecto | Spec-Kit (GitHub) | OpenSpec (Fission AI) |
|---------|-------------------|----------------------|
| **Repositorio** | [github/spec-kit](https://github.com/github/spec-kit) | [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) |
| **Estrellas GitHub** | ~5.000 | 30.000+ |
| **Licencia** | Open source | MIT, open source |
| **Instalacion** | Python (uv/uvx) | Node.js (npm) |
| **Version actual** | 0.7.2 | 1.3.0 |
| **Tipo de proyecto** | Greenfield (nuevo) | Brownfield (existente) |
| **Agentes soportados** | Claude, Copilot, Gemini, +10 | Claude, Copilot, Cursor, OpenCode, +20 |
| **Estructura** | `.specify/` | `openspec/` |
| **Constitucion** | Si (`constitution.md`) | No (usa `config.yaml` con context) |
| **Delta specs** | No | Si (ADDED, MODIFIED, REMOVED) |
| **Archivado** | No | Si (`archive/` con fecha) |
| **Schemas custom** | No | Si (`openspec schema init`) |
| **Idiomas** | Ingles | Multiidioma (ES, PT, ZH, JA, FR, DE) |
| **Git extension** | Si (commits, branches) | No (usa git directo) |
| **Workflows** | Si (workflow.yml) | No |

### Ventajas de Spec-Kit para este proyecto

| Ventaja | Por que importa aqui |
|---------|---------------------|
| **Constitucion** | Define reglas no negociables (SOLID, ACID) que la IA no puede violar. OpenSpec no tiene este concepto |
| **Templates oficiales** | spec-template.md, plan-template.md, tasks-template.md con formato estandar |
| **Git extension** | Comandos /speckit-git-commit, /speckit-git-feature integrados. Util para los 3 estudiantes |
| **Analyze + Checklist** | Valida consistencia entre spec, plan y tasks. Bueno para evaluacion |
| **Fases claras** | Constitution -> Specify -> Plan -> Tasks -> Implement. Facil de ensenar |

### Ventajas de OpenSpec para este proyecto

| Ventaja | Por que importa aqui |
|---------|---------------------|
| **Delta specs** | Cuando un estudiante agrega una feature, solo documenta LO QUE CAMBIA, no reescribe todo |
| **Brownfield** | El proyecto ya tiene codigo. OpenSpec esta disenado para esto |
| **Archivado** | Cada change queda archivado con fecha. Trazabilidad completa |
| **Explore** | `/opsx:explore` permite pensar la idea antes de comprometerse. Bueno para estudiantes |
| **Mas rapido** | `/opsx:propose` genera TODO de una vez (proposal + specs + design + tasks) |
| **npm** | Los estudiantes ya tienen Node.js (para React). No necesitan instalar Python/uv extra |
| **Multiidioma** | Puede generar specs en espanol |

### Desventajas de cada uno

| Herramienta | Desventaja | Impacto |
|-------------|-----------|---------|
| **Spec-Kit** | No tiene delta specs | Hay que reescribir la spec completa para cada cambio |
| **Spec-Kit** | Instalacion mas compleja (Python + uv + uvx) | Los estudiantes pueden tener problemas con uv |
| **Spec-Kit** | Version 0.7.2 (pre-release) | Posibles cambios breaking |
| **Spec-Kit** | Fases con "gates" | Menos flexible que OpenSpec |
| **OpenSpec** | No tiene constitucion | Las reglas no negociables no tienen un lugar dedicado |
| **OpenSpec** | No tiene Git extension | No integra commits/branches como Spec-Kit |
| **OpenSpec** | No tiene Analyze/Checklist | No valida consistencia entre artefactos |
| **OpenSpec** | Requiere Node.js 20.19+ | Puede ser problema si tienen version vieja |

---

## 7. Recomendacion para este proyecto y similares

### Usar AMBAS herramientas, cada una para lo que es mejor:

| Fase del proyecto | Herramienta | Por que |
|-------------------|-------------|---------|
| **Inicio (greenfield)** | Spec-Kit | Constitution + estructura inicial + fases claras |
| **Agregar features (brownfield)** | OpenSpec | Delta specs + propose rapido + archivado |
| **Evaluacion** | Spec-Kit | Analyze + Checklist para verificar completitud |
| **Trabajo en equipo** | Spec-Kit | Git extension para commits/branches estandar |
| **Exploracion de ideas** | OpenSpec | `/opsx:explore` sin comprometerse |
| **Documentacion educativa** | sdd/ (manual) | SOLID, ACID, diagramas Mermaid (ninguna herramienta los genera) |

### Flujo recomendado para estudiantes

```
1. Al inicio del proyecto:
   specify init --here --integration claude    <- Spec-Kit: constitution + estructura
   openspec init                               <- OpenSpec: delta specs + changes

2. Para cada feature nueva:
   /opsx:explore "quiero agregar X"            <- OpenSpec: explorar idea
   /opsx:propose agregar-X                     <- OpenSpec: generar artefactos
   (revisar y ajustar)
   /opsx:apply                                 <- OpenSpec: implementar
   /opsx:archive                               <- OpenSpec: archivar + fusionar

3. Para validar:
   /speckit-analyze                            <- Spec-Kit: consistencia
   /speckit-checklist                          <- Spec-Kit: calidad

4. Para commitear:
   /speckit-git-commit                         <- Spec-Kit: commit estandar
```

### Para proyectos similares (tutoriales universitarios)

| Escenario | Recomendacion |
|-----------|--------------|
| Proyecto nuevo, 1 estudiante | Spec-Kit solo (constitution + specs por feature) |
| Proyecto nuevo, 3+ estudiantes | Spec-Kit (constitution + git extension) + OpenSpec (delta specs para cada estudiante) |
| Proyecto existente, agregar features | OpenSpec solo (delta specs + propose + archive) |
| Curso de Diseno de Software | Ambas + sdd/ manual (para ensenar conceptos: SOLID, ACID, patrones, diagramas) |
| Produccion real | OpenSpec (brownfield, rapido, multiidioma) |

---

## 8. Que instalamos en este proyecto

| Herramienta | Version | Metodo | Fecha |
|------------|---------|--------|-------|
| uv | 0.11.7 | `pip install uv` | 2026-04-14 |
| specify-cli (Spec-Kit) | 0.7.2.dev0 | `uvx --from git+...spec-kit specify init` | 2026-04-14 |
| OpenSpec | 1.3.0 | `npm install -g @fission-ai/openspec@latest` | 2026-04-14 |

### Skills de Claude Code instalados

| De Spec-Kit | De OpenSpec |
|------------|-------------|
| /speckit-constitution | /opsx:explore |
| /speckit-specify | /opsx:propose |
| /speckit-plan | /opsx:apply |
| /speckit-tasks | /opsx:archive |
| /speckit-implement | |
| /speckit-clarify | |
| /speckit-analyze | |
| /speckit-checklist | |
| /speckit-git-commit | |
| /speckit-git-feature | |

---

## 9. Referencias

- OpenSpec repo: [github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
- OpenSpec guia: [webreactiva.com/blog/openspec](https://www.webreactiva.com/blog/openspec)
- Spec-Kit repo: [github.com/github/spec-kit](https://github.com/github/spec-kit)
- Spec-Kit docs: [spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- Video SDD conceptual: [youtu.be/p2WA672HrdI](https://youtu.be/p2WA672HrdI)
- Video Spec-Kit tutorial: [youtu.be/QzSCmSFKvko](https://youtu.be/QzSCmSFKvko)
- Blog Microsoft: [Diving Into SDD](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)
- Seguridad vibe coding: [Awesome Agents Report](https://github.com/nicholasgriffintn/awesome-agents)
