from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .database import Base, session

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(100),nullable=False)
    description = Column(Text,nullable=True)

    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)

    def __init__(self,**args):
        self.title = args['title']
        self.user_id = args['user_id']
        if 'description' in args:
            self.description = args['description']

    def save_to_db(self) -> None:
        session.add(self)
        session.commit()

    def delete_from_db(self) -> None:
        session.delete(self)
        session.commit()
