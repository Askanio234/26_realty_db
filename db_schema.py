from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_reality.sqlite'
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# from sqlalchemy import create_engine
# from sqlalchemy import Column, Integer, String, Boolean, Text, Date, Float
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base


# engine = create_engine('sqlite:///db_reality.sqlite')

# db_session = scoped_session(sessionmaker(bind=engine))

# data_base = declarative_base()

# data_base.query = db_session.query_property()


class Residences(db.Model):
    __tablename__ = 'residences'
    id = db.Column(db.Integer, primary_key=True)
    settlement = db.Column(db.String(150), index=True)
    is_under_construction = db.Column(db.Boolean)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, index=True)
    living_area = db.Column(db.Float)
    premise_area = db.Column(db.Float)
    has_balcony = db.Column(db.Boolean)
    address = db.Column(db.Text)
    construction_year = db.Column(db.Integer)
    rooms_number = db.Column(db.Integer)
    work_id = db.Column(db.Integer, unique=True, index=True)
    is_new = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)

    def __str__(self):
        return "residence in {} with work id - {}".format(
                                            self.settlement,
                                            self.work_id)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
