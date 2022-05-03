from typing import List, Optional
from app.models.aresta import *


class Rota(BaseModel):
    id: Optional[int] = None
    data: List[Aresta]
