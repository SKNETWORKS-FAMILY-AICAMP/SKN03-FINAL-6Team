from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from sympy.physics.units import force

from app.core.config import settings

# SQLAlchemy 설정
Base = declarative_base()

class MessageModel(Base):
    """SQL 대화 기록 모델"""
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    session_id = Column(String(255), index=True, nullable=False)
    message_type = Column(String(255), nullable=False)  # 'human' or 'ai'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# SQLAlchemy 세션 생성
connection_string = f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_URL}:3306/{settings.DATABASE_NAME}"
engine = create_engine(connection_string)  # SQLite 사용
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

class ChatHistoryManager:
    """대화 기록 관리 클래스"""
    def __init__(self, session):
        self.session = session

    def save_message(self, session_id: str, user_id, message: BaseMessage, message_type: str):
        """대화 메시지를 저장"""
        message_record = MessageModel(
            session_id=session_id,
            user_id=user_id,
            message_type=message_type,
            content=message.content
        )
        self.session.add(message_record)
        self.session.commit()

    def load_history(self, session_id: str):
        """대화 기록 불러오기"""
        messages = (
            self.session.query(MessageModel)
            .filter_by(session_id=session_id)
            .order_by(MessageModel.created_at)
            .all()
        )
        # 메시지 타입에 따라 HumanMessage 또는 AIMessage로 변환
        return [
            HumanMessage(content=msg.content) if msg.message_type == "human"
            else AIMessage(content=msg.content)
            for msg in messages
        ]
