from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI(
    title="BibliotecaApiProject ",
    version='0.0.1',
    description="Api desenvolvida na disciplina de Programação Orientado a Objeto II"
)

######################### ROUTERS #####################
from App.views.Autor.Controller import autor
from App.views.Categoria.Controller import categoria
from App.views.Biblioteca.Controller import biblioteca
from App.views.Editora.Controller import editora
from App.views.HistoricoEmprestimos.Controller import historicoEmprestimos
from App.views.Livros.Controller import livros
from App.views.Usuario.Controller import usuario


app.include_router(autor)
app.include_router(categoria)
app.include_router(biblioteca)
app.include_router(editora)
app.include_router(historicoEmprestimos)
app.include_router(livros)
app.include_router(usuario)


@app.get("/apiname", include_in_schema=False, response_class=HTMLResponse)
async def apiname() -> str:
    return "BibliotecaApiProject"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("manage:app", host="0.0.0.0", port=5935, log_level="info", reload=True)
