# OpenSpec - Instalación, Uso y Comparación con Spec-Kit

> OpenSpec es el framework open source de [Fission AI](https://github.com/Fission-AI/OpenSpec)
> para Spec Driven Development (SDD). Con 30.000+ estrellas en GitHub, es compatible con
> 20+ agentes de IA (Claude Code, Cursor, Copilot, Gemini, OpenCode, etc.).
>
> A diferencia de Spec-Kit (GitHub) que es para proyectos nuevos (greenfield),
> OpenSpec está diseñado para proyectos existentes (brownfield) con el concepto
> de **delta specs** — cambios incrementales que no reescriben toda la spec.

---

## 1. Qué es OpenSpec

OpenSpec convierte el SDD en un flujo de trabajo con herramientas reales.
No es una plantilla de Markdown — es una CLI que se instala con npm y se
integra con tu agente de IA.

### 4 principios de OpenSpec

| Principio | Qué significa |
|-----------|-------------|
| **Fluido, no rígido** | No hay puertas de fase. Puedes volver atrás cuando quieras |
| **Iterativo, no waterfall** | Aprende mientras construyes, refina sobre la marcha |
| **Fácil, no complejo** | Configuración mínima, arranque en segundos |
| **Brownfield first** | Diseñado para proyectos existentes, no solo para nuevos |

### 4 conceptos fundamentales

| Concepto | Qué es | Dónde vive |
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

| Herramienta | Versión mínima | Cómo verificar |
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

### 2.4 Qué genera openspec init

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

### 2.5 Desactivar telemetría (opcional)

```powershell
$env:OPENSPEC_TELEMETRY = "0"
```

---

## 3. Comandos de OpenSpec (OPSX)

### Comandos principales (perfil core)

| Comando | Qué hace | Cuándo usarlo |
|---------|----------|--------------|
| `/opsx:explore` | Modo exploratorio libre, sin crear artefactos | Cuando no tienes claro el enfoque |
| `/opsx:propose` | Crea un change con TODOS los artefactos (proposal, specs, design, tasks) | Inicio rápido, la mayoría de los casos |
| `/opsx:apply` | Implementa las tareas del change | Cuando el plan está listo |
| `/opsx:archive` | Archiva el change y fusiona delta specs | Cuando todas las tareas están completas |

### Comandos avanzados (perfil expandido)

| Comando | Qué hace |
|---------|----------|
| `/opsx:new` | Crea solo la estructura del change (sin artefactos) |
| `/opsx:continue` | Genera el siguiente artefacto según dependencias |
| `/opsx:ff` | Fast-forward: genera todos los artefactos de golpe |
| `/opsx:verify` | Valida implementación contra specs |
| `/opsx:sync` | Fusiona delta specs sin archivar |
| `/opsx:bulk-archive` | Archiva varios changes a la vez |
| `/opsx:onboard` | Tutorial guiado con tu propio código |

> **Nota**: En Claude Code se usa dos puntos (`/opsx:propose`).
> En Cursor, OpenCode, Windsurf se usa guión (`/opsx-propose`).

---

## 4. Flujo completo con ejemplo

### Agregar una feature nueva al proyecto existente

```
Paso 1: Explorar la idea
> /opsx:explore
> "Necesito agregar exportación CSV en la página de producto"
> La IA analiza el código existente y sugiere enfoques

Paso 2: Crear el change con artefactos
> /opsx:propose agregar-csv-producto
> Genera:
>   openspec/changes/agregar-csv-producto/
>   ├── proposal.md      <- Por qué y qué
>   ├── specs/            <- Delta specs (qué cambia)
>   ├── design.md         <- Cómo (enfoque técnico)
>   └── tasks.md          <- Checklist de implementación

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

## 6. Comparacion detallada: Manual (sdd/) vs Spec-Kit vs OpenSpec

### Tabla comparativa de los 3 enfoques

| Aspecto | sdd/ (Manual) | Spec-Kit (GitHub) | OpenSpec (Fission AI) |
|---------|---------------|-------------------|----------------------|
| **Quién genera** | El humano escribe todo | La IA llena templates vía /speckit-* | La IA genera artefactos vía /opsx:* |
| **Instalación** | Ninguna (solo crear archivos .md) | Python + uv + uvx | Node.js + npm |
| **Complejidad setup** | Cero | Media (uv puede fallar en Windows) | Baja (npm install y listo) |
| **Formato** | Libre (tu decides la estructura) | Formato fijo (templates oficiales) | Formato fijo (proposal/spec/design/tasks) |
| **Constitución** | Sí (01_constitucion.md, 322 líneas) | Sí (constitution.md, formato oficial) | No (usa config.yaml con context) |
| **Diagramas Mermaid** | Sí (secuencia, clases, ER) | No (falta según el video) | No |
| **SOLID, ACID, patrones** | Sí (explicados con ejemplos) | No (solo si los escribes) | No |
| **Delta specs** | No | No | Sí (ADDED, MODIFIED, REMOVED) |
| **Archivado** | No | No | Sí (archive/ con fecha) |
| **Given/When/Then** | No | Sí (spec-template.md) | Sí (formato BDD) |
| **Paralelización [P]** | Sí (manual) | Sí (tasks-template.md) | Sí (automático) |
| **Git extension** | No | Sí (/speckit-git-*) | No |
| **Analyze/Checklist** | No | Sí (/speckit-analyze) | Sí (/opsx:verify) |
| **Multiidioma** | Sí (escribes en el idioma que quieras) | No (inglés) | Sí (ES, PT, ZH, JA, FR, DE) |
| **Brownfield** | Sí (funciona con cualquier proyecto) | Limitado | Diseñado para esto |
| **Educativo** | Muy alto (tutorial detallado) | Medio (formato estandar) | Medio (formato estandar) |
| **Reproducible** | No (cada quien escribe diferente) | Sí (templates + slash commands) | Sí (propose genera todo igual) |
| **Agentes IA** | Cualquiera (es solo Markdown) | Claude, Copilot, Gemini, +10 | Claude, Copilot, Cursor, +20 |
| **Estrellas GitHub** | N/A | ~5.000 | 30.000+ |
| **Versión** | N/A | 0.7.2 (pre-release) | 1.3.0 (estable) |

### Tabla comparativa: qué tiene cada uno

| Documento/Feature | sdd/ (Manual) | .specify/ (Spec-Kit) | openspec/ (OpenSpec) |
|-------------------|:---:|:---:|:---:|
| Constitución / reglas globales | ✅ 01_constitucion.md | ✅ constitution.md | ❌ (usa config.yaml) |
| Especificación / spec por feature | ✅ 02_especificacion.md | ✅ specs/{feature}/spec.md | ✅ specs/{dominio}/spec.md |
| Clarificación / preguntas | ✅ 03_clarificacion.md | ✅ /speckit-clarify | ✅ /opsx:explore |
| Plan técnico | ✅ 04_plan.md | ✅ specs/{feature}/plan.md | ✅ changes/{nombre}/design.md |
| Tareas ejecutables | ✅ 05_tareas.md | ✅ specs/{feature}/tasks.md | ✅ changes/{nombre}/tasks.md |
| Modelo de datos (SQL) | ✅ data-model.md | ❌ (se crea manual) | ❌ (se crea manual) |
| Diagramas secuencia (Mermaid) | ✅ 04_plan.md secc.7 | ❌ | ❌ |
| Diagrama clases (Mermaid) | ✅ 04_plan.md secc.8 | ❌ | ❌ |
| SOLID explicado con ejemplos | ✅ 01_constitucion.md | ❌ | ❌ |
| ACID explicado | ✅ 01_constitucion.md | ❌ | ❌ |
| Patrones de diseño | ✅ 01_constitucion.md | ❌ | ❌ |
| Delta specs (cambios incrementales) | ❌ | ❌ | ✅ |
| Archivado de cambios | ❌ | ❌ | ✅ |
| Proposal (por que + alcance) | ❌ | ❌ | ✅ changes/{}/proposal.md |
| Given/When/Then (BDD) | ❌ | ✅ | ✅ |
| Git integration (commits/branches) | ❌ | ✅ /speckit-git-* | ❌ |
| Guía de instalación | ✅ 06_specify_cli.md | ✅ GUIA_SPECKIT.md | ✅ 07_openspec.md |

### Ventajas de cada enfoque

**sdd/ (Manual) — Lo mejor para enseñar**

| Ventaja | Por qué |
|---------|---------|
| Total libertad de formato | Puedes incluir SOLID, ACID, patrones, diagramas, lo que quieras |
| No requiere instalación | Solo Markdown, funciona en cualquier editor |
| Diagramas Mermaid | Ni Spec-Kit ni OpenSpec los generan |
| Contenido educativo | Explicaciones con ejemplos, comparaciones, narrativas |
| Cualquier idioma | Escribes en espanol directamente |
| Sin dependencia de herramienta | Si Spec-Kit o OpenSpec desaparecen, tu sdd/ sigue |

**Spec-Kit — Lo mejor para estructura y validación**

| Ventaja | Por qué |
|---------|---------|
| Constitución como concepto formal | Reglas no negociables que la IA respeta |
| Templates estándar | Todos los specs tienen el mismo formato |
| /speckit-analyze | Valida que spec, plan y tasks estén alineados |
| /speckit-checklist | Genera checklist de calidad automático |
| Git extension | Commits y branches estandarizados |
| Fases claras | Fácil de enseñar: 1.Constitution 2.Specify 3.Plan 4.Tasks 5.Implement |

**OpenSpec — Lo mejor para proyectos existentes**

| Ventaja | Por qué |
|---------|---------|
| Delta specs | Solo documentas LO QUE CAMBIA, no reescribes todo |
| /opsx:propose | Genera TODO de una vez (proposal + spec + design + tasks) |
| /opsx:explore | Piensas la idea antes de comprometerte |
| Archivado | Trazabilidad completa con fechas |
| npm install | Fácil de instalar (los estudiantes ya tienen Node.js) |
| Multiidioma | Specs en espanol nativo |
| 30.000+ estrellas | Comunidad activa, actualizaciones frecuentes |

### Desventajas de cada enfoque

| Enfoque | Desventaja | Impacto |
|---------|-----------|---------|
| **Manual (sdd/)** | No es reproducible (cada quien escribe diferente) | Difícil estandarizar en equipos grandes |
| **Manual (sdd/)** | No tiene validación automática | No sabes si spec y código están alineados |
| **Manual (sdd/)** | Requiere disciplina del humano | Si no escribes, no existe |
| **Spec-Kit** | No tiene delta specs | Reescribir spec completa para cada cambio |
| **Spec-Kit** | Pre-release (v0.7.2) | Posibles cambios breaking |
| **Spec-Kit** | uv puede fallar en Windows | Instalación complicada para estudiantes |
| **Spec-Kit** | Sin diagramas Mermaid | Falta visual |
| **OpenSpec** | No tiene constitución | Reglas globales no tienen lugar dedicado |
| **OpenSpec** | No tiene Git extension | No integra commits |
| **OpenSpec** | Requiere Node.js 20.19+ | Versión reciente |

---

### Tabla comparativa general (original Spec-Kit vs OpenSpec)

| Aspecto | Spec-Kit (GitHub) | OpenSpec (Fission AI) |
|---------|-------------------|----------------------|
| **Repositorio** | [github/spec-kit](https://github.com/github/spec-kit) | [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) |
| **Estrellas GitHub** | ~5.000 | 30.000+ |
| **Licencia** | Open source | MIT, open source |
| **Instalación** | Python (uv/uvx) | Node.js (npm) |
| **Versión actual** | 0.7.2 | 1.3.0 |
| **Tipo de proyecto** | Greenfield (nuevo) | Brownfield (existente) |
| **Agentes soportados** | Claude, Copilot, Gemini, +10 | Claude, Copilot, Cursor, OpenCode, +20 |
| **Estructura** | `.specify/` | `openspec/` |
| **Constitución** | Sí (`constitution.md`) | No (usa `config.yaml` con context) |
| **Delta specs** | No | Sí (ADDED, MODIFIED, REMOVED) |
| **Archivado** | No | Sí (`archive/` con fecha) |
| **Schemas custom** | No | Sí (`openspec schema init`) |
| **Idiomas** | Inglés | Multiidioma (ES, PT, ZH, JA, FR, DE) |
| **Git extension** | Sí (commits, branches) | No (usa git directo) |
| **Workflows** | Sí (workflow.yml) | No |

### Ventajas de Spec-Kit para este proyecto

| Ventaja | Por qué importa aquí |
|---------|---------------------|
| **Constitución** | Define reglas no negociables (SOLID, ACID) que la IA no puede violar. OpenSpec no tiene este concepto |
| **Templates oficiales** | spec-template.md, plan-template.md, tasks-template.md con formato estándar |
| **Git extension** | Comandos /speckit-git-commit, /speckit-git-feature integrados. Útil para los 3 estudiantes |
| **Analyze + Checklist** | Valida consistencia entre spec, plan y tasks. Bueno para evaluación |
| **Fases claras** | Constitution -> Specify -> Plan -> Tasks -> Implement. Fácil de enseñar |

### Ventajas de OpenSpec para este proyecto

| Ventaja | Por qué importa aquí |
|---------|---------------------|
| **Delta specs** | Cuando un estudiante agrega una feature, solo documenta LO QUE CAMBIA, no reescribe todo |
| **Brownfield** | El proyecto ya tiene código. OpenSpec está diseñado para esto |
| **Archivado** | Cada change queda archivado con fecha. Trazabilidad completa |
| **Explore** | `/opsx:explore` permite pensar la idea antes de comprometerse. Bueno para estudiantes |
| **Más rápido** | `/opsx:propose` genera TODO de una vez (proposal + specs + design + tasks) |
| **npm** | Los estudiantes ya tienen Node.js (para React). No necesitan instalar Python/uv extra |
| **Multiidioma** | Puede generar specs en espanol |

### Desventajas de cada uno

| Herramienta | Desventaja | Impacto |
|-------------|-----------|---------|
| **Spec-Kit** | No tiene delta specs | Hay que reescribir la spec completa para cada cambio |
| **Spec-Kit** | Instalación más compleja (Python + uv + uvx) | Los estudiantes pueden tener problemas con uv |
| **Spec-Kit** | Version 0.7.2 (pre-release) | Posibles cambios breaking |
| **Spec-Kit** | Fases con "gates" | Menos flexible que OpenSpec |
| **OpenSpec** | No tiene constitución | Las reglas no negociables no tienen un lugar dedicado |
| **OpenSpec** | No tiene Git extension | No integra commits/branches como Spec-Kit |
| **OpenSpec** | No tiene Analyze/Checklist | No valida consistencia entre artefactos |
| **OpenSpec** | Requiere Node.js 20.19+ | Puede ser problema si tienen version vieja |

---

## 7. Recomendación para este proyecto y similares

### Usar AMBAS herramientas, cada una para lo que es mejor:

| Fase del proyecto | Herramienta | Por qué |
|-------------------|-------------|---------|
| **Inicio (greenfield)** | Spec-Kit | Constitution + estructura inicial + fases claras |
| **Agregar features (brownfield)** | OpenSpec | Delta specs + propose rápido + archivado |
| **Evaluación** | Spec-Kit | Analyze + Checklist para verificar completitud |
| **Trabajo en equipo** | Spec-Kit | Git extension para commits/branches estándar |
| **Exploración de ideas** | OpenSpec | `/opsx:explore` sin comprometerse |
| **Documentación educativa** | sdd/ (manual) | SOLID, ACID, diagramas Mermaid (ninguna herramienta los genera) |

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

| Escenario | Recomendación |
|-----------|--------------|
| Proyecto nuevo, 1 estudiante | Spec-Kit solo (constitution + specs por feature) |
| Proyecto nuevo, 3+ estudiantes | Spec-Kit (constitution + git extension) + OpenSpec (delta specs para cada estudiante) |
| Proyecto existente, agregar features | OpenSpec solo (delta specs + propose + archive) |
| Curso de Diseño de Software | Ambas + sdd/ manual (para enseñar conceptos: SOLID, ACID, patrones, diagramas) |
| Producción real | OpenSpec (brownfield, rápido, multiidioma) |

---

## 8. Qué instalamos en este proyecto

| Herramienta | Versión | Método | Fecha |
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
- Spec-Kit documentación: [spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- Video SDD conceptual: [youtu.be/p2WA672HrdI](https://youtu.be/p2WA672HrdI)
- Video Spec-Kit tutorial: [youtu.be/QzSCmSFKvko](https://youtu.be/QzSCmSFKvko)
- Blog Microsoft: [Diving Into SDD](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)
- Seguridad vibe coding: [Awesome Agents Report](https://github.com/nicholasgriffintn/awesome-agents)
