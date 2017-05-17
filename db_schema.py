from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, Text, Date, Float
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///db_reality.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

data_base = declarative_base()

data_base.query = db_session.query_property()


class Residences(data_base):
    __tablename__ = 'residences'
    id = Column(Integer, primary_key=True)
    settlement = Column(String(150), index=True)
    is_under_construction = Column(Boolean)
    description = Column(Text)
    price = Column(Integer, index=True)
    living_area = Column(Float)
    premise_area = Column(Float)
    has_balcony = Column(Boolean)
    address = Column(Text)
    construction_year = Column(Integer)
    rooms_number = Column(Integer)
    work_id = Column(Integer, unique=True, index=True)
    is_new = Column(Boolean)
    is_active = Column(Boolean)

    def __str__(self):
        return "residence in {} with work id - {}".format(
                                            self.settlement,
                                            self.work_id)


if __name__ == '__main__':
    data_base.metadata.drop_all(bind=engine)
    data_base.metadata.create_all(bind=engine)
