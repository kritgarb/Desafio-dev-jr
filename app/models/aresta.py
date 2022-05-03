from pydantic import BaseModel


class Aresta(BaseModel):
    source: str
    target: str
    distance: int
