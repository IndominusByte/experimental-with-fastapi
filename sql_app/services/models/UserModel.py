from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .database import Base, session

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String(100),unique=True,index=True,nullable=False)
    password = Column(String(100),nullable=False)
    is_active = Column(Boolean,default=False)

    items = relationship("Item",backref='user',cascade='all,delete-orphan')

    def __init__(self,**args):
        self.email = args['email']
        self.password = args['password']

    def save_to_db(self) -> None:
        session.add(self)
        session.commit()

    def delete_from_db(self) -> None:
        session.delete(self)
        session.commit()
