# David Willian
from fastapi import APIRouter
from domain.entities.Produto import Produto
import db
from infra.orm.ProdutoModel import ProdutoDB

router = APIRouter()
# Criar as rotas/endpoints: GET, POST, PUT, DELETE

@router.get("/produto/", tags=["Produto"])
async def get_produto():

    try:
        session = db.Session()
        
        #busca todos
        dados = session.query(ProdutoDB).all()
        
        return dados, 200

    except Exception as e:
        return {"Erro":str(e)}, 400
    finally:
        session.close()

@router.get("/produto/{id}", tags=["Produto"])
async def get_produto(id: int):
    try:
        session = db.Session()
        
        # busca um com filtro
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).all()
        
        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/produto/", tags=["Produto"])
async def post_produto(corpo: Produto):
    try:
        session = db.Session()
        
        dados = ProdutoDB(None, corpo.nome, corpo.descricao, corpo.foto, corpo.valor_unitario)
        session.add(dados)
        #sesson.flush()
        session.commit()
        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/produto/{id}", tags=["Produto"])
async def put_produto(id: int, corpo: Produto):
    try:
        session = db.Session()
        
        # busca os dados atuais pelo id
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()
        # atualiza os dados com base no corpo da requisição
        dados.nome = corpo.nome
        dados.descricao = corpo.descricao
        dados.foto = corpo.foto
        dados.valor_unitario = corpo.valor_unitario
        session.add(dados)
        session.commit()
        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/produto/{id}", tags=["Produto"])
async def delete_produto(id: int):
    try:
        session = db.Session()
        # busca os dados atuais pelo id
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()
        session.delete(dados)
        session.commit()
        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()