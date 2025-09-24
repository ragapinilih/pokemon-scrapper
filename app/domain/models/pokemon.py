from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PokemonType:
    name: str


@dataclass
class PokemonStat:
    name: str
    value: int


@dataclass
class PokemonAbility:
    name: str
    is_hidden: bool = False


@dataclass
class Pokemon:
    id: int
    name: str
    types: List[PokemonType]
    stats: List[PokemonStat]
    abilities: List[PokemonAbility]
    height: Optional[int] = None   # in decimetres
    weight: Optional[int] = None   # in hectograms
    base_experience: Optional[int] = None
