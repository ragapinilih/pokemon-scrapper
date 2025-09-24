from database.db import get_cursor

SELECT_COLUMNS = "id, name, type, height, weight"


def map_pokemon_row(row):
    return {
        "id": str(row[0]),
        "name": row[1],
        "type": row[2],
        "height": row[3],
        "weight": row[4],
    }


def fetch_many(query: str, params: tuple):
    with get_cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()
    return [map_pokemon_row(row) for row in rows]


def list_pokemon(limit: int = 20, offset: int = 0):
    query = f"SELECT {SELECT_COLUMNS} FROM pokemon ORDER BY name LIMIT %s OFFSET %s;"
    return fetch_many(query, (limit, offset))


def search_by_name(name: str, limit: int = 20, offset: int = 0):
    query = (
        f"SELECT {SELECT_COLUMNS} FROM pokemon WHERE name LIKE %s "
        f"ORDER BY name LIMIT %s OFFSET %s;"
    )
    return fetch_many(query, (f"%{name}%", limit, offset))

def search_by_type(pokemon_type: str, limit: int = 20, offset: int = 0):
    query = (
        f"SELECT {SELECT_COLUMNS} FROM pokemon WHERE type = %s "
        f"ORDER BY name LIMIT %s OFFSET %s;"
    )
    return fetch_many(query, (pokemon_type, limit, offset))

def upsert_pokemon(pokemon: dict) -> None:
    """Insert or ignore a single pokemon by name."""
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO pokemon (name, type, height, weight)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE
            SET type = EXCLUDED.type,
                height = EXCLUDED.height,
                weight = EXCLUDED.weight;
            """,
            (
                pokemon["name"],
                pokemon.get("type"),
                pokemon.get("height"),
                pokemon.get("weight"),
            ),
        )
