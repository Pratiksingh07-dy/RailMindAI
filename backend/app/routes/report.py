from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.report import Report
from app.schemas.report_schema import ReportCreate
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

security = HTTPBearer()


@router.post("/create")
def create_report(
    report: ReportCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    current_user = get_current_user(
        token,
        db
    )

    if not current_user:
        return {"message": "Invalid token"}

    new_report = Report(
        user_id=current_user.id,
        station_name=report.station_name,
        issue_type=report.issue_type,
        description=report.description
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return {
        "message": "Report created successfully",
        "report_id": new_report.id,
        "created_by": current_user.username
    }


@router.get("/all")
def get_all_reports(db: Session = Depends(get_db)):

    reports = db.query(Report).all()

@router.get("/my-reports")
def get_my_reports(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    current_user = get_current_user(
        token,
        db
    )

    if not current_user:
        return {"message": "Invalid token"}

    reports = db.query(Report).filter(
        Report.user_id == current_user.id
    ).all()


    return reports

