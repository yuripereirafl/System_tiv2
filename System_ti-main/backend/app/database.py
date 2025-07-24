from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base


from app.models.funcionario import Funcionario
from app.models.sistema import Sistema
from app.models.setor import Setor
from app.models.grupo_email import GrupoEmail

SQLALCHEMY_DATABASE_URL = "sqlite:///./system_ti.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Garante que todos os modelos sejam importados antes de criar as tabelas
Base.metadata.create_all(bind=engine)
