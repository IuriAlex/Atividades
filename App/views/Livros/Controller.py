from typing import List
from fastapi import status, APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.dapendencias.dep import get_session
from App.views.models.LivrosModel import LivrosModel
from App.views.schemas.LivrosSchemas import LivrosSchemas

livros = APIRouter(tags=["Livros"])


@livros.post('/CadastrarLivros', status_code=status.HTTP_201_CREATED, response_model=LivrosSchemas)
async def registra_livros(item: LivrosSchemas, db: AsyncSession = Depends(get_session)):
    novo_livros = LivrosModel(idObras=item.idObras, titulo=item.titulo, classificacao=item.classificacao, lingua=item.lingua, midia=item.midia, autorId=item.autorId, editoraId=item.editoraId, categoriaId=item.categoriaId)

    db.add(novo_livros)
    await db.commit()

    return novo_livros


# Todos os livros
@livros.get('/ListarLivros', response_model=List[LivrosSchemas])
async def listar_livros(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LivrosModel)
        result = await session.execute(query)
        Liv_list: List[LivrosModel] = result.scalars().unique().all()

        return Liv_list


# Livros por codigo
@livros.get('/ListarLivros{codigo_livros}', response_model=LivrosSchemas, status_code=status.HTTP_200_OK)
async def list_livros(codigo_livros: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LivrosModel).filter(LivrosModel.codigo == codigo_livros)
        result = await session.execute(query)
        artigo: LivrosModel = result.scalars().unique().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(detail='Livros não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@livros.put('/AlteracaoLivros{codigo_livros}', response_model=LivrosSchemas, status_code=status.HTTP_202_ACCEPTED)
async def alteracao_livros(codigo_livros: int, item: LivrosSchemas, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LivrosModel).filter(LivrosModel.codigo == codigo_livros)
        result = await session.execute(query)
        Liv_up: LivrosModel = result.scalars().unique().one_or_none()

        if Liv_up:
            Liv_up.idObras = item.idObras
	    Liv_up.titulo = item.titulo
	    Liv_up.classificacao = item.classificacao
	    Liv_up.ligua = item.lingua
	    Liv_up.midia = item.midia
	    Liv_up.autorId = item.autorId
	    Liv_up.editoraId = item.editoraId
	    Liv_up.categoriaId = item.categoriaId

            await session.commit()
            return Liv_up
        else:
            raise HTTPException(detail="Código livros não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@livros.delete('/DeletarLivros{codigo_livros}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_livros(codigo_livros: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LivrosModel).filter(LivrosModel.codigo == codigo_livros)
        result = await session.execute(query)
        Liv_del = result.scalar_one_or_none()

        if Liv_del:
            await session.delete(Liv_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Código livros não encontrado.", status_code=status.HTTP_404_NOT_FOUND)
