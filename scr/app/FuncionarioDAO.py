# David Willian
import db
from infra.orm.FuncionarioModel import FuncionarioDB

from fastapi import APIRouter
from domain.entities.Funcionario import Funcionario
router = APIRouter()
# Criar as rotas/endpoints: GET, POST, PUT, DELETE
@router.get("/funcionario/", tags=["Funcionário"])
async def get_funcionario():
    try:
        session = db.Session()

        dados = session.query(FuncionarioDB).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/funcionario/{id}", tags=["Funcionário"])
async def get_funcionario(id: int):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/funcionario/cpf/{cpf}", tags=["Funcionário - Valida CPF"])
async def cpf_funcionario(cpf: str):
    try:
        session = db.Session()

        dados = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == cpf).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/funcionario/login/", tags=["Funcionário - Login"])
async def login_funcionario(corpo: Funcionario):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == corpo.cpf).filter(FuncionarioDB.senha == corpo.senha).one()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/funcionario/", tags=["Funcionário"])
async def post_funcionario(corpo: Funcionario):
    try:
        session = db.Session()
        dados = FuncionarioDB(**corpo.model_dump())

        session.add(dados)
        session.commit()
        return {"id": dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()
            
@router.put("/funcionario/{id}", tags=["Funcionário"])
async def put_funcionario(id: int, corpo: Funcionario):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).one()
        dados.nome = corpo.nome
        dados.cpf = corpo.cpf
        dados.telefone = corpo.telefone
        dados.senha = corpo.senha
        dados.matricula = corpo.matricula
        dados.grupo = corpo.grupo
        session.add(dados)
        session.commit()
        return {"id": dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/funcionario/{id}", tags=["Funcionário"])
async def delete_funcionario(id: int):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).one()
        session.delete(dados)
        session.commit()
        return {"id": dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()