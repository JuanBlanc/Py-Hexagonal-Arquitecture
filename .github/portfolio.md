---
title: Game Match Engine
description: Backend de partidas online escrito como referencia de arquitectura hexagonal, con dos persistencias intercambiables.
slug: game-match-engine
tags: [Python, Falcon, Arquitectura hexagonal, PostgreSQL, WebSocket]
order: 2
---

Backend de partidas online —jugadores, catálogo de juegos, ciclo de vida de la
partida, puntuaciones, ranking y emparejamiento— escrito como plantilla de
referencia de **arquitectura hexagonal**. La gracia no es el dominio, que es
sencillo a propósito, sino que los puertos y adaptadores estén separados de
verdad y no solo en el diagrama del README.

## El interior y el exterior

```
app/
├── core/                    interior: no sabe de HTTP ni de bases de datos
│   ├── domain/              entidades, enums, errores
│   ├── application/         los casos de uso
│   └── ports/
│       ├── inbound/         qué se le puede pedir a la aplicación
│       └── outbound/        qué necesita ella del exterior
├── adapters/                exterior
│   ├── web/                 Falcon ASGI: rutas, recursos, schemas
│   ├── persistence/memory/  repositorios en memoria
│   ├── persistence/postgres/ SQLAlchemy + Alembic
│   ├── messaging/           publicador del ranking en tiempo real
│   └── matchmaking/         proveedor de emparejamiento
└── composition.py           el único módulo que conoce las clases concretas
```

La dirección de las dependencias es una sola:

```
recurso web ─▶ puerto de entrada ─▶ servicio ─▶ puerto de salida ─▶ adaptador
```

Un recurso web depende del puerto de entrada, nunca de la clase del servicio. Un
servicio depende del puerto de salida, nunca del adaptador. Quien une las dos
mitades es `composition.py`, y es el único sitio donde hay un `import` de una
implementación concreta.

## Por qué dos persistencias

Una arquitectura hexagonal con un solo adaptador de almacenamiento es una
promesa sin cobrar. Aquí están los dos —memoria y PostgreSQL con SQLAlchemy y
migraciones de Alembic— implementando los mismos puertos, y el interior no
distingue con cuál está corriendo. Eso es lo que convierte la separación en un
hecho verificable en vez de una intención.

Con el mismo criterio, la transacción se expresa como puerto: un caso de uso
abre una unidad de trabajo y la cierra sin saber si detrás hay una sesión de
SQLAlchemy o un diccionario. Y el ranking en tiempo real llega al WebSocket a
través de un publicador declarado como puerto de salida, así que el dominio
publica un cambio de puntuación sin enterarse de que existen los sockets.

## La API

Jugadores, juegos y partidas con su CRUD; el ciclo de vida de la partida en
`POST /matches/{id}/start|finish|abort`; puntuaciones y ranking por juego; rivales
sugeridos en `GET /players/{id}/opponents`; y el ranking en vivo en
`WS /games/{id}/leaderboard/stream`.

En `docs/bruno/` está la colección completa de peticiones, una por caso de uso:
es la documentación de la API que además se ejecuta.

## Levantarlo

```bash
pip install -r requirements.txt
PYTHONPATH=app uvicorn main:app --reload
```

O `docker compose up --build`, que añade el Postgres.
