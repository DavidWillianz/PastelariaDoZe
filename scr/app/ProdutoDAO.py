# David Willian
from fastapi import APIRouter
from domain.entities.Produto import Produto
router = APIRouter()
# Criar as rotas/endpoints: GET, POST, PUT, DELETE
@router.get("/produto/", tags=["Produto"])
def get_produto():
    return {"msg": "get todos executado"}, 200

@router.get("/produto/{id}", tags=["Produto"])
def get_produto(id: int):
    return {"msg": "get um executado"}, 200

@router.post("/produto/", tags=["Produto"])
def post_produto(corpo: Produto):
    return {"msg": "post executado", "nome": corpo.nome, "descrição": corpo.descricao, "valor":
    corpo.valor_unitario}, 200

@router.put("/produto/{id}", tags=["Produto"])
def put_produto(id: int, corpo: Produto):
    return {"msg": "put executado", "id":id, "nome": corpo.nome, "descrição": corpo.descricao, "valor":
    corpo.valor_unitario}, 200

@router.delete("/produto/{id}", tags=["Produto"])
def delete_produto(id: int):
    return {"msg": "delete executado"}, 200