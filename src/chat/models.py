from src.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Messages(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    message = Column(String)

    def asa_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}