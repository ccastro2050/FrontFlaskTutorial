# Specify CLI - Instalacion y Configuracion

> Este documento registra todo lo que se hizo para instalar y configurar
> [specify-cli](https://github.com/github/spec-kit), la herramienta oficial
> de GitHub para Spec-Driven Development (SDD).

---

## 1. Que es specify-cli

Es la herramienta de linea de comandos de [GitHub Spec-Kit](https://github.com/github/spec-kit)
que automatiza y da estructura al Spec Driven Development. Sirve para:

| Funcion | Que hace |
|---------|----------|
| **Scaffolding** | Crea la estructura `.specify/` con templates, scripts, constituciones |
| **Guardrails** | Verifica que el codigo generado cumpla con la constitucion |
| **Ciclo de vida** | Permite moverse entre las 5 etapas del SDD con comandos |

Referencia: [github.com/github/spec-kit](https://github.com/github/spec-kit)

---

## 2. Prerrequisitos

| Herramienta | Version instalada | Para que |
|------------|-------------------|----------|
| Python | 3.14.0 | Runtime (ya estaba instalado) |
| Git | (ya instalado) | Control de versiones |
| uv | 0.11.7 | Gestor de paquetes Python (se instalo) |
| specify-cli | 0.7.2.dev0 | CLI de Spec-Kit (se instalo via uvx) |

---

## 3. Instalacion paso a paso

### 3.1 Instalar uv (gestor de paquetes)

```powershell
pip install uv
```

uv es el gestor de paquetes recomendado por GitHub para ejecutar specify-cli.
Referencia: [docs.astral.sh/uv](https://docs.astral.sh/uv/)

### 3.2 Verificar que specify-cli funciona

```powershell
# En Windows, necesita PYTHONIOENCODING=utf-8 por los emojis del banner
$env:PYTHONIOENCODING = "utf-8"
uvx --from git+https://github.com/github/spec-kit.git specify version
```

Resultado:
```
CLI Version    0.7.2.dev0
Python         3.14.0
Platform       Windows
Architecture   AMD64
```

### 3.3 Inicializar en el proyecto

```powershell
cd C:\Users\fcl\OneDrive\Desktop\proyectoscsharp\FrontFlaskTutorial
$env:PYTHONIOENCODING = "utf-8"
uvx --from git+https://github.com/github/spec-kit.git specify init --here --ai claude --ignore-agent-tools
```

Opciones usadas:
- `--here`: inicializar en el directorio actual (no crear subcarpeta)
- `--ai claude`: configurar para Claude Code como agente IA
- `--ignore-agent-tools`: no validar herramientas del agente

> Nota: `--ai` esta deprecado en favor de `--integration claude` (desde v1.0.0).

---

## 4. Que genero specify init

### 4.1 Estructura de carpetas creada

```
FrontFlaskTutorial/
├── .specify/                              <- Carpeta principal de Spec-Kit
│   ├── memory/
│   │   └── constitution.md               <- Plantilla de constitucion (por llenar)
│   ├── templates/
│   │   ├── constitution-template.md      <- Template para constituciones
│   │   ├── spec-template.md              <- Template para especificaciones
│   │   ├── plan-template.md              <- Template para planes
│   │   ├── tasks-template.md             <- Template para tareas
│   │   ├── checklist-template.md         <- Template para checklists
│   │   └── agent-file-template.md        <- Template para CLAUDE.md
│   ├── scripts/powershell/
│   │   ├── check-prerequisites.ps1       <- Verificar herramientas
│   │   ├── common.ps1                    <- Funciones compartidas
│   │   ├── create-new-feature.ps1        <- Crear rama feature/
│   │   ├── setup-plan.ps1                <- Configurar plan
│   │   └── update-agent-context.ps1      <- Actualizar contexto del agente
│   ├── extensions/
│   │   └── git/                          <- Extension Git (commits, branches, etc)
│   │       ├── commands/                 <- Comandos git del spec-kit
│   │       └── scripts/                  <- Scripts bash/powershell para git
│   ├── workflows/
│   │   └── speckit/workflow.yml          <- Workflow de Spec-Kit
│   ├── integrations/
│   │   ├── claude.manifest.json          <- Configuracion para Claude Code
│   │   └── claude/scripts/              <- Scripts de integracion con Claude
│   ├── extensions.yml                    <- Registro de extensiones
│   ├── init-options.json                 <- Opciones usadas en init
│   └── integration.json                  <- Integracion activa (claude)
│
├── .claude/skills/                       <- Skills de Claude Code (nuevas)
│   ├── speckit-constitution/SKILL.md     <- /speckit-constitution
│   ├── speckit-specify/SKILL.md          <- /speckit-specify
│   ├── speckit-plan/SKILL.md             <- /speckit-plan
│   ├── speckit-tasks/SKILL.md            <- /speckit-tasks
│   ├── speckit-implement/SKILL.md        <- /speckit-implement
│   ├── speckit-clarify/SKILL.md          <- /speckit-clarify
│   ├── speckit-analyze/SKILL.md          <- /speckit-analyze
│   ├── speckit-checklist/SKILL.md        <- /speckit-checklist
│   ├── speckit-git-commit/SKILL.md       <- /speckit-git-commit
│   ├── speckit-git-feature/SKILL.md      <- /speckit-git-feature
│   ├── speckit-git-initialize/SKILL.md   <- /speckit-git-initialize
│   ├── speckit-git-remote/SKILL.md       <- /speckit-git-remote
│   ├── speckit-git-validate/SKILL.md     <- /speckit-git-validate
│   └── speckit-taskstoissues/SKILL.md    <- /speckit-taskstoissues
│
└── sdd/                                  <- Nuestra documentacion SDD (NO tocada)
    ├── 00_indice.md
    ├── 01_constitucion.md
    ├── 02_especificacion.md
    ├── 03_clarificacion.md
    ├── 04_plan.md
    ├── 05_tareas.md
    └── data-model.md
```

### 4.2 Archivos clave generados

| Archivo | Que es | Estado |
|---------|--------|--------|
| `.specify/memory/constitution.md` | Plantilla de constitucion con placeholders `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]` | Por llenar (tiene placeholders) |
| `.specify/templates/spec-template.md` | Template para crear especificaciones con User Stories y Given/When/Then | Listo para usar |
| `.specify/templates/plan-template.md` | Template para planes tecnicos | Listo para usar |
| `.specify/templates/tasks-template.md` | Template para listas de tareas con marcadores `[P]` | Listo para usar |
| `.specify/init-options.json` | Opciones usadas en `specify init` | Auto-generado |
| `.specify/integration.json` | Integracion activa: `claude` | Auto-generado |

---

## 5. Comandos disponibles (skills de Claude Code)

Despues de `specify init --ai claude`, Claude Code tiene estos slash commands:

### Comandos principales (ciclo SDD)

| Comando | Fase SDD | Que hace |
|---------|----------|----------|
| `/speckit-constitution` | Constitucion | Establece principios no negociables del proyecto |
| `/speckit-specify` | Especificacion | Define requisitos y historias de usuario |
| `/speckit-clarify` | Clarificacion | Hace preguntas para resolver ambiguedades |
| `/speckit-plan` | Plan | Crea plan tecnico con stack elegido |
| `/speckit-tasks` | Tareas | Genera desglose de tareas ejecutables |
| `/speckit-implement` | Codigo | Ejecuta las tareas del plan |

### Comandos de mejora (opcionales)

| Comando | Que hace |
|---------|----------|
| `/speckit-analyze` | Valida consistencia entre artefactos (spec vs plan vs tasks) |
| `/speckit-checklist` | Genera checklists de calidad para validar requisitos |

### Comandos de Git

| Comando | Que hace |
|---------|----------|
| `/speckit-git-commit` | Commit con mensaje estandarizado |
| `/speckit-git-feature` | Crear rama feature/ desde spec |
| `/speckit-git-initialize` | Inicializar repo git |
| `/speckit-git-remote` | Configurar remote |
| `/speckit-git-validate` | Validar estado del repo |

### Comando extra

| Comando | Que hace |
|---------|----------|
| `/speckit-taskstoissues` | Convertir tareas a GitHub Issues |

---

## 6. Comparacion: nuestra carpeta sdd/ vs .specify/

> Nuestra carpeta `sdd/` se creo ANTES de instalar specify-cli.
> Ambas coexisten. `sdd/` tiene contenido real del proyecto;
> `.specify/` tiene plantillas y herramientas del CLI.

| Aspecto | sdd/ (nuestros docs) | .specify/ (Spec-Kit CLI) |
|---------|---------------------|------------------------|
| Contenido | Documentacion REAL del proyecto (llena, con datos concretos) | Plantillas con PLACEHOLDERS (por llenar) |
| Constitucion | `01_constitucion.md` (322 lineas, SOLID, ACID, patrones) | `memory/constitution.md` (plantilla vacia) |
| Especificacion | `02_especificacion.md` (244 lineas, modelo ER, flujos) | `templates/spec-template.md` (formato Given/When/Then) |
| Plan | `04_plan.md` (510 lineas, diagramas secuencia y clases) | `templates/plan-template.md` (estructura vacia) |
| Tareas | `05_tareas.md` (221 lineas, todas completadas) | `templates/tasks-template.md` (formato con [P]) |
| Modelo de datos | `data-model.md` (224 lineas, SQL completo) | No tiene (se crea por feature) |
| Clarificacion | `03_clarificacion.md` (131 lineas, preguntas resueltas) | No tiene (se genera con /speckit-clarify) |
| Skills Claude | No aplica | `.claude/skills/speckit-*/SKILL.md` (14 skills) |
| Scripts | No aplica | `.specify/scripts/powershell/` (5 scripts) |
| Git extension | No aplica | `.specify/extensions/git/` (comandos git) |

### Conclusion

La carpeta `sdd/` es la **documentacion viva del proyecto** — tiene todo el contenido real.
La carpeta `.specify/` es la **infraestructura de Spec-Kit** — tiene templates, scripts y skills
para crear nuevas features siguiendo el flujo SDD.

Para features futuras, se puede usar `/speckit-specify` que creara una carpeta
`.specify/specs/{feature}/` con `spec.md`, `plan.md`, `tasks.md` siguiendo los templates.

---

## 7. Como usar specify-cli en el dia a dia

### Para crear una nueva feature

```powershell
# 1. Iniciar Claude Code en el proyecto
# 2. Usar el slash command:
/speckit-specify   # Describe la feature, Claude genera spec.md
/speckit-plan      # Claude genera plan tecnico
/speckit-tasks     # Claude genera lista de tareas
/speckit-implement # Claude ejecuta las tareas
```

### Para validar consistencia

```powershell
/speckit-analyze   # Revisa que spec, plan y tasks esten alineados
/speckit-checklist # Genera checklist de calidad
```

### Para crear rama y commit

```powershell
/speckit-git-feature  # Crea rama feature/ desde la spec
/speckit-git-commit   # Commit con mensaje estandarizado
```

---

## 8. Referencias

- Repositorio oficial: [github.com/github/spec-kit](https://github.com/github/spec-kit)
- Documentacion SDD: [spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- Guia instalacion: [github.github.com/spec-kit/installation.html](https://github.github.com/spec-kit/installation.html)
- Blog Microsoft: [Diving Into SDD With Spec Kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)
- Paquete npm: [@spec-kit/cli](https://www.npmjs.com/package/@spec-kit/cli)
- Video SDD: [La forma CORRECTA de programar con IA en 2026](https://youtu.be/p2WA672HrdI)
- DeepWiki: [Instalacion Spec-Kit](https://deepwiki.com/github/spec-kit/2.1-installation)

---

## 9. Fecha y version

- **Fecha de instalacion**: 2026-04-14
- **specify-cli version**: 0.7.2.dev0
- **uv version**: 0.11.7
- **Python**: 3.14.0
- **Plataforma**: Windows 11 Pro (AMD64)
- **Integracion**: Claude Code
- **Script type**: PowerShell
