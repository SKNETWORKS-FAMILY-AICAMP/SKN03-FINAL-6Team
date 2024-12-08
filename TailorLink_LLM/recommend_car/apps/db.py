from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# SQLite url 주소
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 초기화
Base.metadata.create_all(bind=engine)

class CarModel(Base):
    # 카 모델 이름 정해지면 이름 적기(임시)
    __tablename__ = "car_models"

    model_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=False)


def get_car_model_by_id(db: Session, model_id: int):
    return db.query(CarModel).filter(CarModel.model_id == model_id).first()