from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

if __name__ == "__main__":
    engine = create_engine('sqlite:///../system_ti.db')
    Base.metadata.create_all(bind=engine)
    print('Tabela usuarios criada com sucesso!')
