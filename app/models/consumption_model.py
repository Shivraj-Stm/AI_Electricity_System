from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Consumption(Base):
    __tablename__ = "consumptions"

    id = Column(Integer, primary_key=True, index=True)
    acct_id = Column(String, ForeignKey("users.acct_id"))
    year = Column(Integer)
    month = Column(String)
    kwh = Column(Integer)

    user = relationship(
        "User",
        back_populates="consumptions"
    )
 