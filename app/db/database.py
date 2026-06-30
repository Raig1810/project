from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, sessionmaker

sqlite_database = "sqlite:///data/database.db"
engine = create_engine(sqlite_database, echo=False)
LocalSession = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    group = Column(String)
    average_score = Column(Float)
    is_active = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)