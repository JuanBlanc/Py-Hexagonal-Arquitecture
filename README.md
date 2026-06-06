# game-match-engine

Plantilla de referencia de **arquitectura hexagonal (Ports & Adapters)** sobre un
backend de partidas online: jugadores, juegos, partidas, puntuaciones y matchmaking.

Es un ejemplo didáctico. El núcleo de negocio no conoce el framework web ni el
almacenamiento; habla con el exterior solo a través de puertos, y los adaptadores
los implementan.

## Estructura

```
app/
├── core/                         interior del hexágono (independiente de tecnología)
│   ├── domain/                   entidades puras, enums, errores
│   ├── application/              servicios = casos de uso
│   └── ports/
│       ├── inbound/              puertos de entrada (driving): qué se le puede pedir a la app
│       └── outbound/             puertos de salida (driven): qué necesita la app del exterior
├── adapters/                     exterior del hexágono
│   ├── web/                      Falcon ASGI: rutas, recursos, schemas (driving)
│   ├── persistence/memory/       repositorios en memoria (driven)
│   ├── messaging/                publicador de leaderboard en tiempo real (driven)
│   └── matchmaking/              proveedor de emparejamiento (driven)
└── composition.py                composition root: une los puertos con sus adaptadores
```

## Flujo de dependencias

```
web (resources)  ─▶  inbound port  ─▶  application service  ─▶  outbound port  ─▶  adapter
```

Un recurso web depende del **puerto de entrada**, nunca de la clase de servicio.
Un servicio depende del **puerto de salida**, nunca del adaptador concreto. El único
módulo que conoce las implementaciones concretas es `composition.py`.

## API

| Método | Ruta | Caso de uso |
|---|---|---|
| GET/POST | `/players` | listar / registrar jugadores |
| GET/PATCH/DELETE | `/players/{player_id}` | consultar / actualizar / borrar |
| GET | `/players/{player_id}/opponents?count=` | sugerir rivales (matchmaking) |
| GET/POST | `/games` | catálogo de juegos |
| GET/DELETE | `/games/{game_id}` | consultar / borrar |
| GET/POST | `/matches` | listar / crear partidas |
| GET | `/matches/{match_id}` | consultar partida |
| POST | `/matches/{match_id}/start\|finish\|abort` | ciclo de vida de la partida |
| GET/POST | `/matches/{match_id}/scores` | listar / enviar puntuaciones |
| GET | `/games/{game_id}/leaderboard?limit=` | ranking del juego |
| WS | `/games/{game_id}/leaderboard/stream` | ranking en tiempo real |

## Ejecutar

```
pip install -r requirements.txt
PYTHONPATH=app uvicorn main:app --reload
```

O con Docker:

```
docker compose up --build
```

## Stack

Python · Falcon ASGI · Pydantic · Docker
