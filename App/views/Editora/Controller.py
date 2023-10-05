from typing import List
from fastapi import status, APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.dapendencias.dep import get_session
from App.views.models.EditoraModel import EditoraModel
from App.views.schemas.EditoraSchemas import EditoraSchemas

editora = APIRouter(tags=["Editora"])


@editora.post('/CadastrarEditora', status_code=status.HTTP_201_CREATED, response_model=EditoraSchemas)
async def registra_editora(item: EditoraSchemas, db: AsyncSession = Depends(get_session)):
    novo_editora = EditoraModel(idEditora=item.idEditora, nome=item.nome, endereco=item.endereco)

    db.add(novo_editora)
    await db.commit()

    return novo_editora


# Todos os editora
@editora.get('/ListarEditora', response_model=List[EditoraSchemas])
async def listar_editora(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EditoraModel)
        result = await session.execute(query)
        Edi_list: List[EditoraModel] = result.scalars().unique().all()

        return Edi_list


# Editora por codigo
@editora.get('/ListarEditora{codigo_editora}', response_model=EditoraSchemas, status_code=status.HTTP_200_OK)
async def list_editora(codigo_editora: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EditoraModel).filter(EditoraModel.codigo == codigo_editora)
        result = await session.execute(query)
        artigo: EditoraModel = result.scalars().unique().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(detail='Editora não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@editora.put('/AlteracaoEditora{codigo_editora}', response_model=EditoraSchemas, status_code=status.HTTP_202_ACCEPTED)
async def alteracao_editora(codigo_editora: int, item: EditoraSchemas, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EditoraModel).filter(EditoraModel.codigo == codigo_editora)
        result = await session.execute(query)
        Edi_up: EditoraModel = result.scalars().unique().one_or_none()

        if Edi_up:
            Edi_up.idEditora = item.idEditora
	    Edi_up.nome = item.nome
	    Edi_up.endereco = item.endereco

            await session.commit()
            return Edi_up
        else:
            raise HTTPException(detail="Código editora não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@editora.delete('/DeletarEditora{codigo_editora}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_editora(codigo_editora: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EditoraModel).filter(EditoraModel.codigo == codigo_editora)
        result = await session.execute(query)
        Edi_del = result.scalar_one_or_none()

        if Edi_del:
            await session.delete(Edi_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Código editora não encontrado.", status_code=status.HTTP_404_NOT_FOUND)
