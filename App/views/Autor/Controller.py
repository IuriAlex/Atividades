from typing import List
from fastapi import status, APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.dapendencias.dep import get_session
from App.views.models.LivrosModel import EstadoModel
from App.views.schemas.HistoricoEmprestimosSchemas import EstadoSchemas

autor = APIRouter(tags=["Autor"])


@autor.post('/CadastrarAutor', status_code=status.HTTP_201_CREATED, response_model=AutorSchemas)
async def registra_autor(item: AutorSchemas, db: AsyncSession = Depends(get_session)):
    novo_autor = AutorModel(idAutor=item.idAutor, nome=item.nome, nacionalidade=item.nacionalidade)

    db.add(novo_autor)
    await db.commit()

    return novo_autor


# Todos os autor
@autor.get('/ListarAutor', response_model=List[AutorSchemas])
async def listar_autor(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AutorModel)
        result = await session.execute(query)
        aut_list: List[AutorModel] = result.scalars().unique().all()

        return aut_list


# Autor por codigo
@autor.get('/ListarAutor{codigo_estado}', response_model=AutorSchemas, status_code=status.HTTP_200_OK)
async def list_autor(codigo_autor: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AutorModel).filter(AutorModel.codigo == codigo_autor)
        result = await session.execute(query)
        artigo: AutorModel = result.scalars().unique().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(detail='Autor não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@autor.put('/AlteracaoAutor{codigo_autor}', response_model=AutorSchemas, status_code=status.HTTP_202_ACCEPTED)
async def alteracao_autor(codigo_autor: int, item: AutorSchemas, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AutorModel).filter(AutorModel.codigo == codigo_autor)
        result = await session.execute(query)
        aut_up: AutorModel = result.scalars().unique().one_or_none()

        if aut_up:
            aut_up.idAutor = item.idAutor
	    aut_up.nome = item.nome
	    aut_up.nacionalidade = item.nacionalidade

            await session.commit()
            return aut_up
        else:
            raise HTTPException(detail="Código estado não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@autor.delete('/DeletarAutor{codigo_autor}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_autor(codigo_autor: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AutorModel).filter(AutorModel.codigo == codigo_autor)
        result = await session.execute(query)
        aut_del = result.scalar_one_or_none()

        if aut_del:
            await session.delete(est_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Código estado não encontrado.", status_code=status.HTTP_404_NOT_FOUND)
