# Colección Bruno — Game Match Engine

Colección [Bruno](https://www.usebruno.com/) para probar la API a mano.

## Abrir

1. Bruno → **Open Collection** → selecciona la carpeta `docs/bruno`.
2. Arriba a la derecha, elige el environment **Local** (`baseUrl = http://localhost:8000`).
3. Arranca la API: `docker compose up --build` (o en local con `PYTHONPATH=app uvicorn main:app --reload`).

## Variables

El environment **Local** define `baseUrl` y `wsUrl`. El resto se capturan solas
en tiempo de ejecución (scripts `post-response`), así que no hay que copiar IDs:

| Variable | La fija | La usan |
|---|---|---|
| `playerId` | Register player | Get/Update/Delete player, Suggest opponents, Create match, Submit score |
| `gameId` | Add game | Get/Delete game, Create match, leaderboard(s) |
| `matchId` | Create match | Get match, Start/Finish/Abort, scores |

`Register player` genera además un `username` único en cada ejecución para no chocar
con `DuplicateEntity`.

## Orden sugerido (flujo completo)

1. **Players → Register player**  (fija `playerId`)
2. **Games → Add game**  (fija `gameId`)
3. **Matches → Create match**  (fija `matchId`)
4. **Matches → Start match**  (la partida pasa a `in_progress`; necesario para puntuar)
5. **Scores → Submit score**  (una o varias veces)
6. **Scores → Game leaderboard**  /  **List match scores**
7. **Matches → Finish match**

## Stream en tiempo real (WebSocket)

El único stream del proyecto es **WebSocket**: `ws://localhost:8000/games/{game_id}/leaderboard/stream`.
El servidor solo **emite**: por cada `Submit score` del juego manda un mensaje JSON.

> **No hay endpoint SSE** en esta API; solo WebSocket. (El recurso es
> `on_websocket` en `app/adapters/web/resources/leaderboard_stream.py`.)

La petición **Stream → Leaderboard stream (WebSocket)** funciona si tu versión de
Bruno trae soporte WebSocket. Para verlo: abre la conexión y, en otra pestaña,
lanza `Submit score` varias veces.

### Fallback por terminal (si tu Bruno no soporta WS)

```bash
# con websocat (recomendado)
websocat "ws://localhost:8000/games/<GAME_ID>/leaderboard/stream"

# o con wscat (npm i -g wscat)
wscat -c "ws://localhost:8000/games/<GAME_ID>/leaderboard/stream"
```

Deja eso escuchando y, en paralelo, envía puntuaciones (Bruno o curl):

```bash
curl -X POST "http://localhost:8000/matches/<MATCH_ID>/scores" \
  -H "Content-Type: application/json" \
  -d '{"player_id":"<PLAYER_ID>","points":1500}'
```

Cada envío debería aparecer como un mensaje en la conexión WebSocket.
