import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from models.pokemon import upsert_pokemon

POKEAPI_BASE = "https://pokeapi.co/api/v2/pokemon"

def get_pokemon_list(limit=50, offset=0):
    """Fetch list of pokemon names from API"""
    url = f"{POKEAPI_BASE}?limit={limit}&offset={offset}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return [p["name"] for p in data["results"]]

def get_pokemon_details(name):
    """Fetch details of a single pokemon"""
    url = f"{POKEAPI_BASE}/{name}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    pokemon_type = data["types"][0]["type"]["name"] if data["types"] else None
    
    return {
        "name": data["name"],
        "type": pokemon_type,
        "height": data["height"],
        "weight": data["weight"]
    }

def insert_pokemon(pokemon):
    """Insert or update pokemon in database via model layer"""
    upsert_pokemon(pokemon)

def scrape_and_store(limit=50, max_workers=10):
    """Scrape pokemon data concurrently and save to DB"""
    pokemon_names = get_pokemon_list(limit=limit)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(get_pokemon_details, name): name for name in pokemon_names}
        
        for future in as_completed(futures):
            name = futures[future]
            try:
                details = future.result()
                insert_pokemon(details)
                print(f"✅ Inserted {details['name']}")
            except Exception as e:
                print(f"❌ Failed to process {name}: {e}")

if __name__ == "__main__":
    import time
    import os

    start_time = time.time()

    try:
        max_workers = len(os.sched_getaffinity(0))
    except AttributeError:
        import multiprocessing
        max_workers = multiprocessing.cpu_count()

    limit = int(os.getenv("POKEMON_SCRAPE_LIMIT", 200))
    scrape_and_store(limit=limit, max_workers=max_workers)

    duration = time.time() - start_time

    print(f"Using max_workers: {max_workers}")
    print(f"⏱️ Duration: {duration:.2f} seconds")
