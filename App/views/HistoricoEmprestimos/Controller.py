from typing import List
from fastapi import status, APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.dapendencias.dep import get_session
from App.views.models.HistoricoEmprestimosModel import HistoricoEmprestimosModel
from App.views.schemas.HistoricoEmprestimosSchemas import HistoricoEmprestimosSchemas

historicoEmprestimos = APIRouter(tags=["HistoricoEmprestimos"])


@historicoEmprestimos.post('/CadastrarHistoricoEmprestimos', status_code=status.HTTP_201_CREATED, response_model=HistoricoEmprestimosSchemas)
async def registra_historicoEmprestimos(item: HistoricoEmprestimosSchemas, db: AsyncSession = Depends(get_session)):
    novo_historicoEmprestimos = HistoricoEmprestimosModel(idEmprestimo=item.idEmprestimo, idUsuario=item.idUsuario, idObras=item.idObras, idCategoria=item.idCategoria, idEditora=item.idEditora, idEmprestimo=item.idEmprestimo, dataEmprestimos=item.dataEmprestimos, dataDevolucao=item.dataDevolucao, status=item.status)

    db.add(novo_historicoEmprestimos)
    await db.commit()

    return novo_historicoEmprestimos


# Todos os historicoEmprestimos
@historicoEmprestimos.get('/ListarHistoricoEmprestimos', response_model=List[HistoricoEmprestimosSchemas])
async def listar_historicoEmprestimos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(HistoricoEmprestimosModel)
        result = await session.execute(query)
        His_list: List[HistoricoEmprestimosModel] = result.scalars().unique().all()

        return His_list


# HistoricoEmprestimos por codigo
@historicoEmprestimos.get('/ListarHistoricoEmprestimos{codigo_historicoEmprestimos}', response_model=HistoricoEmprestimosSchemas, status_code=status.HTTP_200_OK)
async def list_historicoEmprestimos(codigo_historicoEmprestimos: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(HistoricoEmprestimosModel).filter(HistoricoEmprestimosModel.codigo == codigo_historicoEmprestimos)
        result = await session.execute(query)
        artigo: HistoricoEmprestimosModel = result.scalars().unique().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(detail='HistoricoEmprestimos não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@historicoEmprestimos.put('/AlteracaoHistoricoEmprestimos{codigo_historicoEmprestimos}', response_model=HistoricoEmprestimosSchemas, status_code=status.HTTP_202_ACCEPTED)
async def alteracao_historicoEmprestimos(codigo_historicoEmprestimos: int, item: HistoricoEmprestimosSchemas, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(HistoricoEmprestimosModel).filter(HistoricoEmprestimosModel.codigo == codigo_historicoEmprestimos)
        result = await session.execute(query)
        His_up: HistoricoEmprestimosModel = result.scalars().unique().one_or_none()

        if His_up:
            His_up.idEmprestimo = item.idEmprestimo
	    His_up.idUsuario = item.idUsuario
	    His_up.idObras = item.idObras
	    His_up.idCategoria = item.idCategoria
	    His_up.idEditora = item.idEditora
	    His_up.idEmprestimo = item.idEmprestimo
	    His_up.dataEmprestimo = item.dataEmprestimo
	    His_up.dataDevolucao = item.dataDevolucao
	    His_up.status = item.status

            await session.commit()
            return His_up
        else:
            raise HTTPException(detail="Código historicoEmprestimos não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@historicoEmprestimos.delete('/DeletarHistoricoEmprestimos{codigo_historicoEmprestimos}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_historicoEmprestimos(codigo_historicoEmprestimos: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(HistoricoEmprestimosModel).filter(HistoricoEmprestimosModel.codigo == codigo_historicoEmprestimos)
        result = await session.execute(query)
        His_del = result.scalar_one_or_none()

        if His_del:
            await session.delete(His_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Código historicoEmprestimos não encontrado.", status_code=status.HTTP_404_NOT_FOUND)
