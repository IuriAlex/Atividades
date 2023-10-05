from typing import List
from fastapi import status, APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.dapendencias.dep import get_session
from App.views.models.UsuarioModel import UsuarioModel
from App.views.schemas.UsuarioSchemas import UsuarioSchemas

usuario = APIRouter(tags=["Usuario"])


@usuario.post('/CadastrarUsuario', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemas)
async def registra_usuario(item: UsuarioSchemas, db: AsyncSession = Depends(get_session)):
    novo_usuario = UsuarioModel(idUsuario=item.idUsuario, nome=item.nome, endereco=item.endereco, telefone=item.telefone, cpf=item.cpf, grupo=item.grupo)

    db.add(novo_usuario)
    await db.commit()

    return novo_usuario


# Todos os usuario
@usuario.get('/ListarUsuario', response_model=List[UsuarioSchemas])
async def listar_usuario(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        Usu_list: List[UsuarioModel] = result.scalars().unique().all()

        return Usu_list


# Usuario por codigo
@usuario.get('/ListarUsuario{codigo_usuario}', response_model=UsuarioSchemas, status_code=status.HTTP_200_OK)
async def list_usuario(codigo_usuario: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.codigo == codigo_usuario)
        result = await session.execute(query)
        artigo: UsuarioModel = result.scalars().unique().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(detail='Usuario não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@usuario.put('/AlteracaoUsuario{codigo_usuario}', response_model=UsuarioSchemas, status_code=status.HTTP_202_ACCEPTED)
async def alteracao_usuario(codigo_usuario: int, item: UsuarioSchemas, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.codigo == codigo_usuario)
        result = await session.execute(query)
        Usu_up: UsuarioModel = result.scalars().unique().one_or_none()

        if Usu_up:
            Usu_up.idUsuario = item.idUsuario
	    Usu_up.nome = item.nome
	    Usu_up.endereco = item.endereco
	    Usu_up.telefone = item.telefone
	    Usu_up.cpf = item.cpf
	    Usu_up.grupo = item.grupo

            await session.commit()
            return Usu_up
        else:
            raise HTTPException(detail="Código usuario não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@usuario.delete('/DeletarUsuario{codigo_usuario}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_usuario(codigo_usuario: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.codigo == codigo_usuario)
        result = await session.execute(query)
        Usu_del = result.scalar_one_or_none()

        if Usu_del:
            await session.delete(Usu_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Código usuario não encontrado.", status_code=status.HTTP_404_NOT_FOUND)
