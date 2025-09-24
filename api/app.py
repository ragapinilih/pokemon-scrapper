from fastapi import FastAPI, HTTPException, Query

from models.pokemon import list_pokemon as model_list_pokemon, search_by_name, search_by_type

app = FastAPI()

SELECT_COLUMNS = "id, name, type, height, weight"

def map_pokemon_row(row):
    return {
        "id": str(row[0]),
        "name": row[1],
        "type": row[2],
        "height": row[3],
        "weight": row[4]
    }

def fetch_pokemon_many(query: str, params: tuple):
    with get_cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()
    return [map_pokemon_row(row) for row in rows]

def get_all_pokemon(limit: int = 20, offset: int = 0):
    return model_list_pokemon(limit=limit, offset=offset)

def get_pokemon_by_name(name: str, limit: int = 20, offset: int = 0):
    return search_by_name(name=name, limit=limit, offset=offset)

    
def get_pokemon_by_type(pokemon_type: str, limit: int = 20, offset: int = 0):
    return search_by_type(pokemon_type=pokemon_type, limit=limit, offset=offset)

@app.get("/pokemon")
async def list_pokemon(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    name: str | None = None,
    pokemon_type: str | None = None
):
    try:
        if name:
            pokemons = get_pokemon_by_name(name=name, limit=limit, offset=offset)
        elif pokemon_type:
            pokemons = get_pokemon_by_type(pokemon_type=pokemon_type, limit=limit, offset=offset)
        else:
            pokemons = get_all_pokemon(limit=limit, offset=offset)
        return {"pokemon": pokemons, "limit": limit, "offset": offset}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))