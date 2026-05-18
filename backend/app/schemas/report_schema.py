from pydantic import BaseModel

class ReportCreate(BaseModel):
    station_name: str
    issue_type: str
    description: str

class ReportUpdate(BaseModel):
    station_name: str
    issue_type: str
    description: str    