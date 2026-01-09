from sqlalchemy import create_engine, Column, String, Float, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DB_PATH = "sqlite:///data/portfolio.db"

engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    fair_value = Column(Float, nullable=True)
    purchase_date = Column(Date, default=datetime.date.today)

Base.metadata.create_all(engine)

def add_position(ticker, quantity, purchase_price, fair_value):
    session = Session()
    position = Position(
        ticker=ticker.upper(),
        quantity=quantity,
        purchase_price=purchase_price,
        fair_value=fair_value
    )
    session.add(position)
    session.commit()
    session.close()

def get_positions():
    session = Session()
    positions = session.query(Position).all()
    session.close()
    return positions

