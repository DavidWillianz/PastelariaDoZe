# David Willian
from pydantic import BaseModel

class Produto(BaseModel):
    id_produto: int = None
    nome: str
    descricao: str = None
    foto: None
    valor_unitario: int