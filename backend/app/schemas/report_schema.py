from pydantic import BaseModel


class ReportCreate(BaseModel):
    station_name: str
    issue_type: str
    description: str
    status: str = "Pending"
    priority: str = "Medium"


class ReportUpdate(BaseModel):
    station_name: str
    issue_type: str
    description: str
    status: str
    priority: str

class ReportStatusUpdate(BaseModel):
    status: str    