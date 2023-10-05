from typing import List
from fastapi import status, APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.dapendencias.dep import get_session
from App.views.models.BibliotecaModel import BibliotecaModel
from App.views.schemas.BibliotecaSchemas import BibliotecaSchemas

biblioteca = APIRouter(tags=["Biblioteca"])


@biblioteca.post('/CadastrarBiblioteca', status_code=status.HTTP_201_CREATED, response_model=BibliotecaSchemas)
async def registra_biblioteca(item: BibliotecaSchemas, db: AsyncSession = Depends(get_session)):
    novo_biblioteca = BibliotecaModel(idBiblioteca=item.idBiblioteca, idUsuario=item.idUsuario, idObras=item.idObras)

    db.add(novo_biblioteca)
    await db.commit()

    return novo_biblioteca


# Todos os biblioteca
@biblioteca.get('/ListarBiblioteca', response_model=List[BibliotecaSchemas])
async def listar_biblioteca(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(BibliotecaModel)
        result = await session.execute(query)
        Bib_list: List[BibliotecaModel] = result.scalars().unique().all()

        return Bib_list


# Biblioteca por codigo
@biblioteca.get('/ListarBiblioteca{codigo_biblioteca}', response_model=BibliotecaSchemas, status_code=status.HTTP_200_OK)
async def list_biblioteca(codigo_biblioteca: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(BibliotecaModel).filter(BibliotecaModel.codigo == codigo_biblioteca)
        result = await session.execute(query)
        artigo: BibliotecaModel = result.scalars().unique().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(detail='Biblioteca não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@biblioteca.put('/AlteracaoBiblioteca{codigo_biblioteca}', response_model=BibliotecaSchemas, status_code=status.HTTP_202_ACCEPTED)
async def alteracao_biblioteca(codigo_biblioteca: int, item: BibliotecaSchemas, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(BibliotecaModel).filter(BibliotecaModel.codigo == codigo_biblioteca)
        result = await session.execute(query)
        Bib_up: BibliotecaModel = result.scalars().unique().one_or_none()

        if Bib_up:
            Bib_up.idBiblioteca = item.idBiblioteca
	    Bib_up.idUsuario = item.idUsuario
	    Bib_up.idObras = item.idObras

            await session.commit()
            return Bib_up
        else:
            raise HTTPException(detail="Código biblioteca não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@biblioteca.delete('/DeletarBiblioteca{codigo_biblioteca}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_biblioteca(codigo_biblioteca: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(BibliotecaModel).filter(BibliotecaModel.codigo == codigo_biblioteca)
        result = await session.execute(query)
        Bib_del = result.scalar_one_or_none()

        if Bib_del:
            await session.delete(Bib_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Código biblioteca não encontrado.", status_code=status.HTTP_404_NOT_FOUND)
