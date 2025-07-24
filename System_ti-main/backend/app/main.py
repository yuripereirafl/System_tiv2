from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.funcionario import router as funcionario_router
from app.routes.sistema import router as sistema_router
from app.routes.setores import router as setores_router
from app.routes.grupo_email import router as grupo_email_router
from app.routes.usuario import router as usuario_router

app = FastAPI()

# Permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique os IPs do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(funcionario_router)
app.include_router(sistema_router)
app.include_router(setores_router)
app.include_router(grupo_email_router)
app.include_router(usuario_router)

@app.get('/')
def read_root():
    return {"message": "API do Sistema TI funcionando!"}
