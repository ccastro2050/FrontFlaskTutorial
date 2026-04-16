# Implementation Plan: Layout y Navegacion

**Status**: Completed

## Components

| Archivo | Responsabilidad |
|---------|----------------|
| `templates/layout/base.html` | Layout base: sidebar + top-row + content + Bootstrap CDN |
| `templates/components/nav_menu.html` | Menu lateral colapsable |
| `templates/pages/home.html` | Pagina inicio (extiende base.html) |
| `routes/home.py` | Blueprint para / |
| `static/css/app.css` | Variables CSS, estilos custom |

## Patron: Template Method (Jinja2)

base.html define la estructura, cada pagina llena `{% block content %}`.
