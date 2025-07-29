from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from ..models.funcionario import Funcionario as FuncionarioModel
from ..models.setor import Setor
from ..models.sistema import Sistema as SistemaModel
from ..models.grupo_email import GrupoEmail
from ..models.grupo_pasta import GrupoPasta
from ..schemas.funcionario import FuncionarioCreate, Funcionario as FuncionarioSchema
from ..schemas.sistema import Sistema as SistemaSchema
from ..schemas.setor import SetorOut
from ..schemas.grupo_email import GrupoEmailOut
from ..schemas.grupo_pasta import GrupoPastaOut
from ..database import engine

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@router.post('/funcionarios/', response_model=FuncionarioSchema)
def adicionar_funcionario(funcionario: FuncionarioCreate):
    db = SessionLocal()
    print(f"[LOG] Valor recebido para data_inclusao: {funcionario.data_inclusao} (type: {type(funcionario.data_inclusao)})")
    # Aceita data_inclusao no formato 'YYYY-MM-DD' e salva como string
    data_inclusao = ''
    if hasattr(funcionario, 'data_inclusao') and funcionario.data_inclusao:
        # Se vier no formato 'YYYY-MM-DD', usa direto, sem conversão
        if isinstance(funcionario.data_inclusao, str) and len(funcionario.data_inclusao) == 10 and funcionario.data_inclusao[4] == '-':
            data_inclusao = funcionario.data_inclusao
        else:
            # Se vier como datetime ou outro formato, converte para string
            data_inclusao = str(funcionario.data_inclusao)
    else:
        data_inclusao = str(datetime.now().date())
    print(f"[LOG] Valor processado para data_inclusao (antes de salvar): {data_inclusao} (type: {type(data_inclusao)})")
    novo_funcionario = FuncionarioModel(
        nome=funcionario.nome,
        sobrenome=funcionario.sobrenome,
        cargo=funcionario.cargo,
        celular=funcionario.celular,
        email=funcionario.email,
        data_inclusao=data_inclusao,
        data_inativado=str(funcionario.data_inativado) if funcionario.data_inativado is not None else ''
    )
    print(f"[LOG] Valor salvo no banco para data_inclusao: {novo_funcionario.data_inclusao} (type: {type(novo_funcionario.data_inclusao)})")
    db.add(novo_funcionario)
    db.commit()
    db.refresh(novo_funcionario)
    # Vincula setores
    if funcionario.setores_ids:
        setores = db.query(Setor).filter(Setor.id.in_(funcionario.setores_ids)).all()
        novo_funcionario.setores = setores
    else:
        novo_funcionario.setores = []
    # Vincula sistemas
    if funcionario.sistemas_ids:
        sistemas = db.query(SistemaModel).filter(SistemaModel.id.in_(funcionario.sistemas_ids)).all()
        novo_funcionario.sistemas = sistemas
    else:
        novo_funcionario.sistemas = []
    # Vincula grupos de e-mail
    if funcionario.grupos_email_ids:
        grupos = db.query(GrupoEmail).filter(GrupoEmail.id.in_(funcionario.grupos_email_ids)).all()
        novo_funcionario.grupos_email = grupos
    else:
        novo_funcionario.grupos_email = []
    # Vincula grupos de pasta
    if hasattr(funcionario, 'grupos_pasta_ids') and funcionario.grupos_pasta_ids:
        grupos_pasta = db.query(GrupoPasta).filter(GrupoPasta.id.in_(funcionario.grupos_pasta_ids)).all()
        novo_funcionario.grupos_pasta = grupos_pasta
    else:
        novo_funcionario.grupos_pasta = []
    db.commit()
    db.refresh(novo_funcionario)
    # Remove _sa_instance_state do dict antes de passar para o Pydantic
    funcionario_dict = dict(novo_funcionario.__dict__)
    funcionario_dict.pop('_sa_instance_state', None)
    funcionario_schema = FuncionarioSchema.model_validate({
        **funcionario_dict,
        'setores': [SetorOut.from_orm(setor) for setor in novo_funcionario.setores],
        'sistemas': [SistemaSchema.from_orm(sistema) for sistema in novo_funcionario.sistemas],
        'grupos_email': [GrupoEmailOut.from_orm(grupo) for grupo in novo_funcionario.grupos_email],
        'grupos_pasta': [GrupoPastaOut.from_orm(grupo) for grupo in novo_funcionario.grupos_pasta],
        'data_inclusao': str(novo_funcionario.data_inclusao) if novo_funcionario.data_inclusao is not None else '',
        'data_inativado': str(novo_funcionario.data_inativado) if novo_funcionario.data_inativado is not None else ''
    })
    db.close()
    return funcionario_schema

@router.get('/funcionarios/{id}/sistemas', response_model=list[SistemaSchema])
def get_funcionario_sistemas(id: int):
    db = SessionLocal()
    funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == id).first()
    if funcionario:
        sistemas = funcionario.sistemas
    else:
        sistemas = []
    db.close()
    return sistemas

@router.get('/funcionarios/', response_model=list[FuncionarioSchema])
def list_funcionarios():
    db = SessionLocal()
    funcionarios = db.query(FuncionarioModel).all()
    resultado = []
    for funcionario in funcionarios:
        setores = [SetorOut.from_orm(setor) for setor in funcionario.setores]
        sistemas = [SistemaSchema.from_orm(sistema) for sistema in funcionario.sistemas]
        grupos_email = [GrupoEmailOut.from_orm(grupo) for grupo in funcionario.grupos_email]
        grupos_pasta = [GrupoPastaOut.from_orm(grupo) for grupo in funcionario.grupos_pasta]
        funcionario_schema = FuncionarioSchema.model_validate({
            **funcionario.__dict__,
            'setores': setores,
            'sistemas': sistemas,
            'grupos_email': grupos_email,
            'grupos_pasta': grupos_pasta,
            'data_inclusao': str(funcionario.data_inclusao) if funcionario.data_inclusao is not None else '',
            'data_inativado': str(funcionario.data_inativado) if funcionario.data_inativado is not None else ''
        })
        resultado.append(funcionario_schema)
    db.close()
    return resultado

@router.put('/funcionarios/{id}', response_model=FuncionarioSchema)
def atualizar_funcionario(id: int, funcionario: FuncionarioCreate):
    db = SessionLocal()
    db_funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == id).first()
    if not db_funcionario:
        db.close()
        raise HTTPException(status_code=404, detail='Funcionário não encontrado')
    db_funcionario.nome = funcionario.nome
    db_funcionario.sobrenome = funcionario.sobrenome
    db_funcionario.cargo = funcionario.cargo
    db_funcionario.celular = funcionario.celular
    db_funcionario.email = funcionario.email
    print(f"[LOG] Valor recebido para data_inativado: {funcionario.data_inativado} (type: {type(funcionario.data_inativado)})")
    if funcionario.data_inativado:
        db_funcionario.data_inativado = str(funcionario.data_inativado)
    else:
        db_funcionario.data_inativado = ''
    print(f"[LOG] Valor salvo no banco para data_inativado: {db_funcionario.data_inativado} (type: {type(db_funcionario.data_inativado)})")
    # Atualiza grupos de e-mail
    if funcionario.grupos_email_ids:
        grupos = db.query(GrupoEmail).filter(GrupoEmail.id.in_(funcionario.grupos_email_ids)).all()
        db_funcionario.grupos_email = grupos
    else:
        db_funcionario.grupos_email = []
    # Atualiza grupos de pasta
    if hasattr(funcionario, 'grupos_pasta_ids') and funcionario.grupos_pasta_ids:
        grupos_pasta = db.query(GrupoPasta).filter(GrupoPasta.id.in_(funcionario.grupos_pasta_ids)).all()
        db_funcionario.grupos_pasta = grupos_pasta
    else:
        db_funcionario.grupos_pasta = []
    # Atualiza setores
    if funcionario.setores_ids:
        setores = db.query(Setor).filter(Setor.id.in_(funcionario.setores_ids)).all()
        db_funcionario.setores = setores
    else:
        db_funcionario.setores = []
    # Atualiza sistemas
    if funcionario.sistemas_ids:
        sistemas = db.query(SistemaModel).filter(SistemaModel.id.in_(funcionario.sistemas_ids)).all()
        db_funcionario.sistemas = sistemas
    else:
        db_funcionario.sistemas = []
    db.commit()
    db.refresh(db_funcionario)
    funcionario_schema = FuncionarioSchema.model_validate({
        **db_funcionario.__dict__,
        'setores': [SetorOut.from_orm(setor) for setor in db_funcionario.setores],
        'sistemas': [SistemaSchema.from_orm(sistema) for sistema in db_funcionario.sistemas],
        'grupos_email': [GrupoEmailOut.from_orm(grupo) for grupo in db_funcionario.grupos_email],
        'grupos_pasta': [GrupoPastaOut.from_orm(grupo) for grupo in db_funcionario.grupos_pasta],
        'data_inclusao': str(db_funcionario.data_inclusao) if db_funcionario.data_inclusao is not None else '',
        'data_inativado': str(db_funcionario.data_inativado) if db_funcionario.data_inativado is not None else ''
    })
    db.close()
    return funcionario_schema

@router.delete('/funcionarios/{id}')
def excluir_funcionario(id: int):
    db = SessionLocal()
    db_funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == id).first()
    if not db_funcionario:
        db.close()
        raise HTTPException(status_code=404, detail='Funcionário não encontrado')
    db.delete(db_funcionario)
    db.commit()
    db.close()
    return {'ok': True}

