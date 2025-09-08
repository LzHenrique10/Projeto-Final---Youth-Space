from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

# Importações dos módulos locais
import models
import schemas
from database import SessionLocal, engine, get_db

# Cria as tabelas no banco de dados (se não existirem)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gerenciamento Escolar",
    description="Uma API completa para gerenciar alunos, professores, cursos, turmas e matrículas.",
    version="1.0.0"
)

# --- Endpoints ---

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento Escolar! Acesse /docs para a documentação."}

# --- CRUD para Professores ---
@app.post("/professores/", response_model=schemas.ProfessorSchema, status_code=status.HTTP_201_CREATED, tags=["Professores"])
def create_professor(professor: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    if db.query(models.Professor).filter(models.Professor.email == professor.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    db_professor = models.Professor(**professor.dict())
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

@app.get("/professores/", response_model=List[schemas.ProfessorSchema], tags=["Professores"])
def read_professores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Professor).offset(skip).limit(limit).all()

@app.get("/professores/{professor_id}", response_model=schemas.ProfessorSchema, tags=["Professores"])
def read_professor(professor_id: int, db: Session = Depends(get_db)):
    db_professor = db.query(models.Professor).filter(models.Professor.id_professor == professor_id).first()
    if db_professor is None: raise HTTPException(status_code=404, detail="Professor não encontrado")
    return db_professor

@app.put("/professores/{professor_id}", response_model=schemas.ProfessorSchema, tags=["Professores"])
def update_professor(professor_id: int, professor: schemas.ProfessorUpdate, db: Session = Depends(get_db)):
    db_professor = db.query(models.Professor).filter(models.Professor.id_professor == professor_id).first()
    if not db_professor: raise HTTPException(status_code=404, detail="Professor não encontrado")
    
    update_data = professor.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_professor, key, value)
        
    db.commit()
    db.refresh(db_professor)
    return db_professor

@app.delete("/professores/{professor_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Professores"])
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    db_professor = db.query(models.Professor).filter(models.Professor.id_professor == professor_id).first()
    if not db_professor: raise HTTPException(status_code=404, detail="Professor não encontrado")
    db.delete(db_professor)
    db.commit()

# --- CRUD para Alunos ---
@app.post("/alunos/", response_model=schemas.AlunoSchema, status_code=status.HTTP_201_CREATED, tags=["Alunos"])
def create_aluno(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    if db.query(models.Aluno).filter(models.Aluno.email == aluno.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    db_aluno = models.Aluno(**aluno.dict())
    db.add(db_aluno)
    db.commit(); db.refresh(db_aluno)
    return db_aluno

@app.get("/alunos/", response_model=List[schemas.AlunoSchema], tags=["Alunos"])
def read_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Aluno).offset(skip).limit(limit).all()

@app.get("/alunos/{aluno_id}", response_model=schemas.AlunoSchema, tags=["Alunos"])
def read_aluno(aluno_id: int, db: Session = Depends(get_db)):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id_aluno == aluno_id).first()
    if db_aluno is None: raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return db_aluno

@app.put("/alunos/{aluno_id}", response_model=schemas.AlunoSchema, tags=["Alunos"])
def update_aluno(aluno_id: int, aluno: schemas.AlunoUpdate, db: Session = Depends(get_db)):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id_aluno == aluno_id).first()
    if not db_aluno: raise HTTPException(status_code=404, detail="Aluno não encontrado")
    update_data = aluno.dict(exclude_unset=True)
    for key, value in update_data.items(): setattr(db_aluno, key, value)
    db.commit(); db.refresh(db_aluno)
    return db_aluno

@app.delete("/alunos/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Alunos"])
def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id_aluno == aluno_id).first()
    if not db_aluno: raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(db_aluno)
    db.commit()

# --- CRUD para Cursos ---
@app.post("/cursos/", response_model=schemas.CursoSchema, status_code=status.HTTP_201_CREATED, tags=["Cursos"])
def create_curso(curso: schemas.CursoCreate, db: Session = Depends(get_db)):
    if db.query(models.Curso).filter(models.Curso.nome == curso.nome).first():
        raise HTTPException(status_code=400, detail="Nome do curso já existe")
    db_curso = models.Curso(**curso.dict())
    db.add(db_curso); db.commit(); db.refresh(db_curso)
    return db_curso

@app.get("/cursos/", response_model=List[schemas.CursoSchema], tags=["Cursos"])
def read_cursos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Curso).offset(skip).limit(limit).all()

@app.get("/cursos/{curso_id}", response_model=schemas.CursoSchema, tags=["Cursos"])
def read_curso(curso_id: int, db: Session = Depends(get_db)):
    db_curso = db.query(models.Curso).filter(models.Curso.id_curso == curso_id).first()
    if db_curso is None: raise HTTPException(status_code=404, detail="Curso não encontrado")
    return db_curso

@app.delete("/cursos/{curso_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Cursos"])
def delete_curso(curso_id: int, db: Session = Depends(get_db)):
    db_curso = db.query(models.Curso).filter(models.Curso.id_curso == curso_id).first()
    if not db_curso: raise HTTPException(status_code=404, detail="Curso não encontrado")
    db.delete(db_curso)
    db.commit()
    
# --- CRUD para Turmas ---
@app.post("/turmas/", response_model=schemas.TurmaSchema, status_code=status.HTTP_201_CREATED, tags=["Turmas"])
def create_turma(turma: schemas.TurmaCreate, db: Session = Depends(get_db)):
    if not db.query(models.Curso).filter(models.Curso.id_curso == turma.id_curso).first(): raise HTTPException(status_code=404, detail="Curso não encontrado")
    if not db.query(models.Professor).filter(models.Professor.id_professor == turma.id_professor).first(): raise HTTPException(status_code=404, detail="Professor não encontrado")
    db_turma = models.Turma(**turma.dict())
    db.add(db_turma); db.commit(); db.refresh(db_turma)
    return db_turma

@app.get("/turmas/", response_model=List[schemas.TurmaDetalhesSchema], tags=["Turmas"])
def read_turmas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Turma).options(joinedload(models.Turma.curso), joinedload(models.Turma.professor)).offset(skip).limit(limit).all()
    
@app.get("/turmas/{turma_id}", response_model=schemas.TurmaDetalhesSchema, tags=["Turmas"])
def read_turma(turma_id: int, db: Session = Depends(get_db)):
    db_turma = db.query(models.Turma).options(joinedload(models.Turma.curso), joinedload(models.Turma.professor)).filter(models.Turma.id_turma == turma_id).first()
    if db_turma is None: raise HTTPException(status_code=404, detail="Turma não encontrada")
    return db_turma
    
@app.delete("/turmas/{turma_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Turmas"])
def delete_turma(turma_id: int, db: Session = Depends(get_db)):
    db_turma = db.query(models.Turma).filter(models.Turma.id_turma == turma_id).first()
    if not db_turma: raise HTTPException(status_code=404, detail="Turma não encontrada")
    db.delete(db_turma)
    db.commit()
    
# --- CRUD para Matrículas ---
@app.post("/matriculas/", response_model=schemas.MatriculaSchema, status_code=status.HTTP_201_CREATED, tags=["Matrículas"])
def create_matricula(matricula: schemas.MatriculaCreate, db: Session = Depends(get_db)):
    if not db.query(models.Aluno).filter(models.Aluno.id_aluno == matricula.id_aluno).first(): raise HTTPException(status_code=404, detail="Aluno não encontrado")
    if not db.query(models.Turma).filter(models.Turma.id_turma == matricula.id_turma).first(): raise HTTPException(status_code=404, detail="Turma não encontrada")
    if db.query(models.Matricula).filter(models.Matricula.id_aluno == matricula.id_aluno, models.Matricula.id_turma == matricula.id_turma).first():
        raise HTTPException(status_code=400, detail="Aluno já matriculado nesta turma")
    db_matricula = models.Matricula(**matricula.dict())
    db.add(db_matricula); db.commit(); db.refresh(db_matricula)
    return db_matricula

@app.get("/matriculas/", response_model=List[schemas.MatriculaDetalhesSchema], tags=["Matrículas"])
def read_matriculas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Matricula).options(joinedload(models.Matricula.aluno), joinedload(models.Matricula.turma).joinedload(models.Turma.curso), joinedload(models.Matricula.turma).joinedload(models.Turma.professor)).offset(skip).limit(limit).all()

@app.delete("/matriculas/{matricula_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Matrículas"])
def delete_matricula(matricula_id: int, db: Session = Depends(get_db)):
    db_matricula = db.query(models.Matricula).filter(models.Matricula.id_matricula == matricula_id).first()
    if not db_matricula: raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    db.delete(db_matricula)
    db.commit()
    
# --- Consultas Avançadas ---
@app.get("/turmas/{turma_id}/alunos", response_model=List[schemas.AlunoSchema], tags=["Consultas Avançadas"])
def get_alunos_por_turma(turma_id: int, db: Session = Depends(get_db)):
    turma = db.query(models.Turma).filter(models.Turma.id_turma == turma_id).first()
    if not turma: raise HTTPException(status_code=404, detail="Turma não encontrada")
    return [matricula.aluno for matricula in turma.matriculas]

@app.get("/alunos/{aluno_id}/turmas", response_model=List[schemas.TurmaDetalhesSchema], tags=["Consultas Avançadas"])
def get_turmas_por_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(models.Aluno).filter(models.Aluno.id_aluno == aluno_id).first()
    if not aluno: raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return [matricula.turma for matricula in aluno.matriculas]

@app.get("/professores/{professor_id}/turmas", response_model=List[schemas.TurmaDetalhesSchema], tags=["Consultas Avançadas"])
def get_turmas_por_professor(professor_id: int, db: Session = Depends(get_db)):
    professor = db.query(models.Professor).options(joinedload(models.Professor.turmas).joinedload(models.Turma.curso)).filter(models.Professor.id_professor == professor_id).first()
    if not professor: raise HTTPException(status_code=404, detail="Professor não encontrado")
    return professor.turmas

