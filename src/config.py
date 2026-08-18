from typing import List

from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    world_list: List[str] = ["Ustebra", "Gentebra"]
    towns_list: List[str] = ["Thais", "Yalahar", "Port Hope", "Venore"]
    characters_list: List[str] = ["Sher Hadesh", "Erikin Knightblood", "Buudx"]

settings = Settings()