from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ATENÇÃO: Substitua com suas credenciais do MySQL.
DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/youth_space"
# Exemplo: "mysql+mysqlconnector://root:minha_senha@localhost:3306/escola_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
