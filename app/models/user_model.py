from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    acct_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    mobile = Column(String, unique=True, index=True)
    tariff_type = Column(String)      # TARIFF_TYPE
    s_t = Column(String)              # S/T
    mtr_srl_no = Column(String, unique=True, index=True)
    load = Column(Integer)
    metr_status = Column(String)      # METR_STATUS

    password = Column(String, nullable=True)
    is_registered = Column(Boolean, default=False)
    role = Column(String, default="customer")

    consumptions = relationship(
        "Consumption",
        back_populates="user",
        cascade="all, delete"
    )