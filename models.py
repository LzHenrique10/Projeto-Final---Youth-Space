from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base

class Professor(Base):
    __tablename__ = "professores"
    id_professor = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    especializacao = Column(String(100))
    turmas = relationship("Turma", back_populates="professor")

class Aluno(Base):
    __tablename__ = "alunos"
    id_aluno = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    status = Column(String(50), nullable=False, default='ativo')
    matriculas = relationship("Matricula", back_populates="aluno", cascade="all, delete-orphan")

class Curso(Base):
    __tablename__ = "cursos"
    id_curso = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, nullable=False, index=True)
    descricao = Column(Text)
    turmas = relationship("Turma", back_populates="curso", cascade="all, delete-orphan")

class Turma(Base):
    __tablename__ = "turmas"
    id_turma = Column(Integer, primary_key=True, index=True)
    id_curso = Column(Integer, ForeignKey("cursos.id_curso"), nullable=False)
    id_professor = Column(Integer, ForeignKey("professores.id_professor"), nullable=False)
    carga_horaria = Column(Integer, nullable=False)
    horario = Column(String(100))
    sala = Column(String(50))
    status = Column(String(50), nullable=False, default='inscrições abertas')
    
    curso = relationship("Curso", back_populates="turmas")
    professor = relationship("Professor", back_populates="turmas")
    matriculas = relationship("Matricula", back_populates="turma", cascade="all, delete-orphan")

class Matricula(Base):
    __tablename__ = "matriculas"
    __table_args__ = (UniqueConstraint('id_aluno', 'id_turma', name='_aluno_turma_uc'),)
    id_matricula = Column(Integer, primary_key=True, index=True)
    id_aluno = Column(Integer, ForeignKey("alunos.id_aluno"), nullable=False)
    id_turma = Column(Integer, ForeignKey("turmas.id_turma"), nullable=False)

    aluno = relationship("Aluno", back_populates="matriculas")
    turma = relationship("Turma", back_populates="matriculas")
