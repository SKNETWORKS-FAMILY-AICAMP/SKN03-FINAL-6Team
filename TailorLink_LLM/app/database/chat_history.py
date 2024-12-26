from sqlalchemy import Column, Integer, String, Text, DateTime, func
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from app.database.mysql import Base, get_db_session
from sqlalchemy.exc import SQLAlchemyError
from pymysql import MySQLError

# 데이터베이스 모델 정의
class MessageModel(Base):
    """SQL 대화 기록 모델"""
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), index=True, nullable=False)
    session_id = Column(String(255), index=True, nullable=False)
    message_type = Column(String(255), nullable=False)  # 'human' or 'ai'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 대화 기록 관리 클래스
class ChatHistoryManager:
    """대화 기록 관리 클래스"""
    def save_message(self, session_id: str, user_id: str, message: BaseMessage, message_type: str):
        """대화 메시지 저장"""
        with get_db_session() as session:
            try:
                message_record = MessageModel(
                    session_id=session_id,
                    user_id=user_id,
                    message_type=message_type,
                    content=message.content,
                )
                session.add(message_record)
                session.commit()
            except SQLAlchemyError as e:
                raise RuntimeError(f"Failed to save message: {e}")

    def load_history(self, session_id: str):
        """대화 기록 불러오기"""
        with get_db_session() as session:
            try:
                messages = (
                    session.query(MessageModel)
                    .filter_by(session_id=session_id)
                    .order_by(MessageModel.created_at)
                    .limit(20)
                    .all()
                )
                return [
                    HumanMessage(content=msg.content) if msg.message_type == "human"
                    else AIMessage(content=msg.content)
                    for msg in messages
                ]
            except SQLAlchemyError as e:
                raise RuntimeError(f"Failed to load history: {e}")
