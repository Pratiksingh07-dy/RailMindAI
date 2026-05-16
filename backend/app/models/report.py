from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    station_name = Column(String)

    issue_type = Column(String)

    description = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )