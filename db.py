from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float
from sqlalchemy.orm import mapper, sessionmaker, declarative_base


Base = declarative_base()
class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    img_url = Column(Integer)
    rating = Column(Float)
    rank = Column(Integer)
    year = Column(String(255))
    age_rating = Column(String(255))
    runtime = Column(String(255))

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title


engine = create_engine('sqlite:///movies.db')
Base.metadata.create_all(engine)