# Spec Driven Development (SDD) - FrontFlaskTutorial

## Que es SDD

Spec Driven Development invierte la estructura de poder en el desarrollo de software: **las especificaciones son el artefacto principal y el codigo es su expresion**. En vez de que el codigo sea la fuente de verdad, la documentacion lo es.

> "Necesitamos pasar a una forma estandarizada de decirle a la IA: 'estas son las reglas de mi proyecto, no puedes saltartelas'. Eso es el SDD."

### Referencia: GitHub Spec-Kit

Este proyecto sigue la metodologia [Spec-Kit de GitHub](https://github.com/github/spec-kit), el toolkit oficial para Spec-Driven Development. La estructura de archivos, las fases y los formatos siguen el estandar de Spec-Kit.

Fuentes:
- Repositorio oficial: [github.com/github/spec-kit](https://github.com/github/spec-kit)
- Documento tecnico: [spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- Blog Microsoft: [Diving Into Spec-Driven Development With GitHub Spec Kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)
- Video: [La forma CORRECTA de programar con IA en 2026: SDD](https://youtu.be/p2WA672HrdI)

---

## Las fases del SDD (segun Spec-Kit)

| # | Fase | Comando Spec-Kit | Que se hace | Documento |
|---|------|-----------------|-------------|-----------|
| 1 | **Constitucion** | `/speckit.constitution` | Reglas no negociables: tecnologias, convenciones, prohibiciones. Es lo PRIMERO que lee la IA | [01_constitucion.md](01_constitucion.md) |
| 2 | **Especificacion** | `/speckit.specify` | Que quieres construir, que problema resuelve, para quien | [02_especificacion.md](02_especificacion.md) |
| 3 | **Clarificacion** | `/speckit.clarify` | La IA hace preguntas sobre lo que olvidaste. Te fuerza a pensar | [03_clarificacion.md](03_clarificacion.md) |
| 4 | **Plan** | `/speckit.plan` | Plan tecnico: estructura, dependencias, orden de implementacion | [04_plan.md](04_plan.md) |
| 5 | **Tareas y Codigo** | `/speckit.tasks` + `/speckit.implement` | Lista de tareas ejecutables, luego la IA escribe el codigo | [05_tareas.md](05_tareas.md) |

### Principio central

> "Lo mas importante del SDD es que la documentacion es un entregable que se versiona, y el codigo es el resultado de esta documentacion."

---

## Estructura de archivos SDD en este proyecto

Siguiendo la estructura de [Spec-Kit](https://github.com/github/spec-kit):

```
FrontFlaskTutorial/
├── sdd/                              <- Carpeta SDD (equivale a .specify/)
│   ├── 00_indice.md                  <- ESTE ARCHIVO: indice y referencias
│   ├── 01_constitucion.md            <- Reglas no negociables (constitution.md)
│   ├── 02_especificacion.md          <- Que se construye (spec.md)
│   ├── 03_clarificacion.md           <- Preguntas y decisiones (clarify)
│   ├── 04_plan.md                    <- Plan tecnico (plan.md)
│   └── 05_tareas.md                  <- Tareas ejecutables (tasks.md)
├── Paso0_PlanDeDesarrollo.md         <- Plan de desarrollo y buenas practicas
├── Paso1_ConceptosBasicos.md         <- Conceptos Flask, Jinja2, Blueprint
├── ...                               <- Pasos 2-11 (tutorial paso a paso)
├── Paso12_LoginYControlDeAcceso.md   <- Login, JWT, BCrypt, middleware
└── app.py, config.py, routes/, ...   <- Codigo fuente (RESULTADO de las specs)
```

### Relacion entre los Pasos (.md) y las fases SDD

| Paso del tutorial | Fase SDD | Que define |
|-------------------|----------|------------|
| Paso 0 | Constitucion | Reglas de trabajo, ramas, convenciones |
| Paso 1-2 | Especificacion | Conceptos, herramientas, que se va a construir |
| Paso 3 | Plan | Crear proyecto, estructura de carpetas |
| Paso 4-10 | Tareas + Codigo | Implementar cada funcionalidad (CRUD, layout, factura) |
| Paso 11 | (Resumen) | Verificacion de que todo funciona |
| Paso 12 | Especificacion + Plan | Login, seguridad, JWT (funcionalidad compleja) |

---

## Proyecto: FrontFlaskTutorial

| Aspecto | Valor |
|---------|-------|
| Nombre | FrontFlaskTutorial |
| Tipo | Frontend web educativo (tutorial paso a paso) |
| Stack | Python 3 + Flask + Jinja2 + Bootstrap 5 |
| API | ApiGenericaCsharp en `http://localhost:5035` |
| BD | PostgreSQL 17 (compatible con SqlServer) |
| Puerto | 5300 |
| Repositorio | GitHub |
| Audiencia | Estudiantes de Diseno de Software (universitarios) |
| Metodologia | Spec Driven Development (Spec-Kit de GitHub) |

---

## Por que SDD para este proyecto

Segun [spec-driven.md de GitHub](https://github.com/github/spec-kit/blob/main/spec-driven.md):

> "No se trata de reemplazar desarrolladores — se trata de amplificar su efectividad automatizando la traduccion mecanica de especificacion a implementacion."

Aplicado a este proyecto:

1. **Es un tutorial**: cada paso debe estar documentado ANTES de codificar
2. **Trabajan 3 estudiantes**: la constitucion define reglas claras para no pisarse
3. **Usa IA para generar codigo**: sin spec, la IA inventa arquitectura y nombres
4. **Se replica en 5 frameworks**: Flask, Blazor, Java, PHP, React — la spec es reutilizable
5. **Es evaluable**: la spec permite verificar si el resultado cumple lo pedido
6. **Reduce retrabajo**: de 40-60% (sin spec) a 10-15% (con spec)
