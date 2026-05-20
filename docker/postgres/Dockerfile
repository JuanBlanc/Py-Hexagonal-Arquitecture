# Imagen oficial de Postgres + extensión TimescaleDB instalada por encima
# (en vez de la imagen timescale/timescaledb que ya la trae precompilada).
FROM postgres:16

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates gnupg wget lsb-release \
    && echo "deb https://packagecloud.io/timescale/timescaledb/debian/ $(lsb_release -c -s) main" \
        > /etc/apt/sources.list.d/timescaledb.list \
    && wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey \
        | gpg --dearmor -o /etc/apt/trusted.gpg.d/timescaledb.gpg \
    && apt-get update \
    && apt-get install -y --no-install-recommends timescaledb-2-postgresql-16 \
    && apt-get purge -y --auto-remove wget lsb-release \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# TimescaleDB necesita cargarse como librería precargada al arrancar Postgres.
# Se activa con `command:` en docker-compose: -c shared_preload_libraries=timescaledb
