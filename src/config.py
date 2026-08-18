from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    world_list = ["Ustebra", "Gentebra"]
    towns_list = ["Thais", "Yalahar", "Port Hope", "Venore"]
    characters_list = ["Sher Hadesh", "Erikin Knightblood", "Buudx"]

settings = Settings()