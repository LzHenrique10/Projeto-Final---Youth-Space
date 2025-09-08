from typing import List, Optional
from pydantic import BaseModel, EmailStr

# --- Schemas para Professor ---
class ProfessorBase(BaseModel):
    nome: str
    email: EmailStr
    especializacao: Optional[str] = None

class ProfessorCreate(ProfessorBase): pass

class ProfessorUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    especializacao: Optional[str] = None

class ProfessorSchema(ProfessorBase):
    id_professor: int
    class Config: orm_mode = True

# --- Schemas para Aluno ---
class AlunoBase(BaseModel):
    nome: str
    email: EmailStr
    status: Optional[str] = 'ativo'

class AlunoCreate(AlunoBase): pass

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[str] = None

class AlunoSchema(AlunoBase):
    id_aluno: int
    class Config: orm_mode = True

# --- Schemas para Curso ---
class CursoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

class CursoCreate(CursoBase): pass

class CursoSchema(CursoBase):
    id_curso: int
    class Config: orm_mode = True

# --- Schemas para Turma ---
class TurmaBase(BaseModel):
    id_curso: int
    id_professor: int
    carga_horaria: int
    horario: Optional[str] = None
    sala: Optional[str] = None
    status: Optional[str] = 'inscrições abertas'

class TurmaCreate(TurmaBase): pass

class TurmaSchema(TurmaBase):
    id_turma: int
    class Config: orm_mode = True

# --- Schemas para Matrícula ---
class MatriculaBase(BaseModel):
    id_aluno: int
    id_turma: int

class MatriculaCreate(MatriculaBase): pass

class MatriculaSchema(MatriculaBase):
    id_matricula: int
    class Config: orm_mode = True

# --- Schemas para Respostas Detalhadas (com relacionamentos) ---
class TurmaDetalhesSchema(TurmaSchema):
    curso: CursoSchema
    professor: ProfessorSchema

class MatriculaDetalhesSchema(MatriculaSchema):
    aluno: AlunoSchema
    turma: TurmaDetalhesSchema
