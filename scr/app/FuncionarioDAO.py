# David Willian
from fastapi import APIRouter
from domain.entities.Funcionario import Funcionario
import db
from infra.orm.FuncionarioModel import FuncionarioDB

from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User
from security import verify_password

router = APIRouter(dependencies=[Depends(get_current_active_user)])

@router.get("/funcionario/", tags=["Funcionário"], dependencies=[Depends(get_current_active_user)], )
async def get_funcionario(current_user:Annotated[User, Depends(get_current_active_user)]):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).all()
        return dados, 200
    except Exception as e:
        return {"Erro":str(e)}, 400
    finally:
        session.close()

@router.get("/funcionario/{id}", tags=["Funcionário"])
async def get_funcionario(id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).all()
        
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/funcionario/", tags=["Funcionário"])
async def post_funcionario(corpo: Funcionario, current_user: Annotated[User, Depends(get_current_active_user)]):
    try:
        session = db.Session()
        
        dados = FuncionarioDB(None, corpo.nome, corpo.matricula, corpo.cpf, corpo.telefone, corpo.grupo, corpo.senha)
        session.add(dados)
        session.commit()
        return {"id": dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/funcionario/{id}", tags=["Funcionário"])
async def put_funcionario(id: int, corpo: Funcionario, current_user: Annotated[User, Depends(get_current_active_user)]):
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
async def delete_funcionario(id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
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
 
@router.post("/funcionario/login/", tags=["Funcionário - Login"])
async def login_funcionario(corpo: Funcionario):
    try:
        session = db.Session()

        funcionario = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == corpo.cpf).first()
        if not funcionario:
            return {"erro": "Funcionário não encontrado"}, 404

        if not verify_password(corpo.senha, funcionario.senha):
            return {"erro": "Senha incorreta"}, 401
        return {
            "id_funcionario": funcionario.id,
            "nome": funcionario.nome,
            "matricula": funcionario.matricula,
            "cpf": funcionario.cpf,
            "telefone": funcionario.telefone,
            "grupo": funcionario.grupo,
        }, 200

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/funcionario/cpf/{cpf}", tags=["Funcionário - Valida CPF"])
async def cpf_funcionario(cpf: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == cpf).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()