from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.report import Report
from app.schemas.report_schema import ReportCreate

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.post("/create")
def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):

    new_report = Report(
        user_id=1,
        station_name=report.station_name,
        issue_type=report.issue_type,
        description=report.description
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return {
        "message": "Report created successfully",
        "report_id": new_report.id
    }