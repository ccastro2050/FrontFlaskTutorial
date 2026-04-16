# Implementation Plan: API Service

**Feature**: 004-api-service
**Status**: Completed

## Components

| Archivo | Responsabilidad |
|---------|----------------|
| `services/api_service.py` | Clase ApiService con listar, crear, actualizar, eliminar |

## Patron: Facade

ApiService es una fachada sobre la API REST. El usuario no necesita saber de HTTP, headers, JSON.
Solo llama metodos simples: `api.listar("producto")`.

## Endpoints consumidos

| Metodo ApiService | HTTP | Endpoint API |
|-------------------|------|-------------|
| listar(tabla) | GET | /api/{tabla}?limite=N |
| crear(tabla, datos) | POST | /api/{tabla} |
| actualizar(tabla, pk, val, datos) | PUT | /api/{tabla}/{pk}/{val} |
| eliminar(tabla, pk, val) | DELETE | /api/{tabla}/{pk}/{val} |
