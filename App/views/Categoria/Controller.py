from typing import List
from fastapi import status, APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.dapendencias.dep import get_session
from App.views.models.CategoriaModel import CategoriaModel
from App.views.schemas.CategoriaSchemas import CategoriaSchemas

categoria = APIRouter(tags=["Categoria"])


@categoria.post('/CadastrarCategoria', status_code=status.HTTP_201_CREATED, response_model=CategoriaSchemas)
async def registra_categoria(item: CategoriaSchemas, db: AsyncSession = Depends(get_session)):
    novo_categoria = CategoriaModel(idCategoria=item.idCategoria, nome=item.nome)

    db.add(novo_categoria)
    await db.commit()

    return novo_categoria


# Todos os categoria
@categoria.get('/ListarCategoria', response_model=List[CategoriaSchemas])
async def listar_categoria(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CategoriaModel)
        result = await session.execute(query)
        Cat_list: List[CategoriaModel] = result.scalars().unique().all()

        return Cat_list


# Categoria por codigo
@categoria.get('/ListarCategoria{codigo_categoria}', response_model=CategoriaSchemas, status_code=status.HTTP_200_OK)
async def list_categoria(codigo_categoria: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CategoriaModel).filter(CategoriaModel.codigo == codigo_categoria)
        result = await session.execute(query)
        artigo: CategoriaModel = result.scalars().unique().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(detail='Categoria não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@categoria.put('/AlteracaoCategoria{codigo_categoria}', response_model=CategoriaSchemas, status_code=status.HTTP_202_ACCEPTED)
async def alteracao_categoria(codigo_categoria: int, item: CategoriaSchemas, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CategoriaModel).filter(CategoriaModel.codigo == codigo_categoria)
        result = await session.execute(query)
        Cat_up: CategoriaModel = result.scalars().unique().one_or_none()

        if Cat_up:
            Cat_up.idCategoria = item.idCategoria
	    Cat_up.nome = item.nome

            await session.commit()
            return Cat_up
        else:
            raise HTTPException(detail="Código categoria não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@categoria.delete('/DeletarCategoria{codigo_categoria}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_categoria(codigo_categoria: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CategoriaModel).filter(CategoriaModel.codigo == codigo_categoria)
        result = await session.execute(query)
        Cat_del = result.scalar_one_or_none()

        if Cat_del:
            await session.delete(Cat_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Código categoria não encontrado.", status_code=status.HTTP_404_NOT_FOUND)
