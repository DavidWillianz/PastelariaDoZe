# David Willian
from pydantic import BaseModel

class Funcionario(BaseModel):
    id_funcionario: int = None
    nome: str
    matricula: str
    cpf: str
    telefone: str = None
    grupo: int # 1 - Administrador, 2 - Gerente, 3 - Funcionario
    senha: str = None