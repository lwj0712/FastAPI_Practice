from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)


# Create tables
Base.metadata.create_all(bind=engine)


# Pydantic schema
class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


class ItemResponse(ItemCreate):
    id: int

    class Config:
        orm_mode = True


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD operations
@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())  # item을 dict로 변환하여 Item 모델로 생성
    db.add(db_item)  # 데이터베이스에 추가(저장X, 세션에만 추가)
    db.commit()  # 데이터베이스에 변경사항 저장
    db.refresh(db_item)  # 데이터베이스에서 최신 정보로 업데이트
    # refresh는 동기화, 주로 전체 데이터를 다시 불러올 때 사용
    return db_item


@app.get("/items/", response_model=list[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
