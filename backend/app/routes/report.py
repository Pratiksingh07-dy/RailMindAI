from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func


from app.database.database import get_db
from app.models.report import Report
from app.schemas.report_schema import (
    ReportCreate,
    ReportUpdate,
    ReportStatusUpdate
)
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

security = HTTPBearer()


# CREATE REPORT
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
    description=report.description,
    status=report.status,
    priority=report.priority
)

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return {
        "message": "Report created successfully",
        "report_id": new_report.id,
        "created_by": current_user.username
    }


# GET ALL REPORTS
@router.get("/all")
def get_all_reports(db: Session = Depends(get_db)):

    reports = db.query(Report).all()

    return reports


# GET MY REPORTS
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


# DELETE REPORT
@router.delete("/{report_id}")
def delete_report(
    report_id: int,
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

    report = db.query(Report).filter(
        Report.id == report_id
    ).first()

    if not report:
        return {"message": "Report not found"}

    if report.user_id != current_user.id:
        return {"message": "You cannot delete another user's report"}

    db.delete(report)
    db.commit()

    return {
        "message": "Report deleted successfully"
    }


# UPDATE REPORT
@router.put("/{report_id}")
def update_report(
    report_id: int,
    updated_report: ReportUpdate,
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

    report = db.query(Report).filter(
        Report.id == report_id
    ).first()

    if not report:
        return {"message": "Report not found"}

    if report.user_id != current_user.id:
        return {"message": "You cannot edit another user's report"}

    report.station_name = updated_report.station_name
    report.issue_type = updated_report.issue_type
    report.description = updated_report.description
    report.status = updated_report.status
    report.priority = updated_report.priority

    db.commit()
    db.refresh(report)

    return {
        "message": "Report updated successfully",
        "updated_report": report.id
    }

@router.get("/filter")
def filter_reports(
    status: str = Query(None),
    priority: str = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Report)

    if status:
        query = query.filter(
            Report.status == status
        )

    if priority:
        query = query.filter(
            Report.priority == priority
        )

    reports = query.all()

    return reports

@router.get("/stats")
def report_stats(
    db: Session = Depends(get_db)
):

    total_reports = db.query(Report).count()

    active_reports = db.query(
        Report
    ).filter(
        Report.status == "Active"
    ).count()

    pending_reports = db.query(
        Report
    ).filter(
        Report.status == "Pending"
    ).count()

    resolved_reports = db.query(
        Report
    ).filter(
        Report.status == "Resolved"
    ).count()

    high_priority = db.query(
        Report
    ).filter(
        Report.priority == "High"
    ).count()

    medium_priority = db.query(
        Report
    ).filter(
        Report.priority == "Medium"
    ).count()

    low_priority = db.query(
        Report
    ).filter(
        Report.priority == "Low"
    ).count()

    return {
        "total_reports": total_reports,
        "active_reports": active_reports,
        "pending_reports": pending_reports,
        "resolved_reports": resolved_reports,
        "high_priority": high_priority,
        "medium_priority": medium_priority,
        "low_priority": low_priority
    }

@router.get("/station/{station_name}")
def get_station_reports(
    station_name: str,
    db: Session = Depends(get_db)
):

    reports = db.query(
        Report
    ).filter(
        Report.station_name == station_name
    ).all()

    return reports    

@router.put("/resolve/{report_id}")
def resolve_report(
    report_id: int,
    status_data: ReportStatusUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    current_user = get_current_user(
        token,
        db
    )

    if not current_user:
        return {
            "message":"Invalid token"
        }

    if current_user.role != "admin":
        return {
            "message":"Admin only"
        }

    report = db.query(
        Report
    ).filter(
        Report.id == report_id
    ).first()

    if not report:
        return {
            "message":"Report not found"
        }

    report.status = status_data.status

    db.commit()
    db.refresh(report)

    return {
        "message":"Report status updated",
        "new_status": report.status
    }

@router.get("/dashboard-stats")
def dashboard_stats(
    db: Session = Depends(get_db)
):

    total_reports = db.query(
        Report
    ).count()

    pending_reports = db.query(
        Report
    ).filter(
        Report.status == "Pending"
    ).count()

    active_reports = db.query(
        Report
    ).filter(
        Report.status == "Active"
    ).count()

    resolved_reports = db.query(
        Report
    ).filter(
        Report.status == "Resolved"
    ).count()

    return {
        "total_reports": total_reports,
        "pending_reports": pending_reports,
        "active_reports": active_reports,
        "resolved_reports": resolved_reports
    }

@router.get("/incident-count")
def incident_count(
    db: Session = Depends(get_db)
):

    data = db.query(
        Report.issue_type,
        func.count(Report.id)
    ).group_by(
        Report.issue_type
    ).all()

    result = []

    for issue, count in data:
        result.append(
            {
                "issue_type": issue,
                "count": count
            }
        )

    return result

@router.get("/paginated")
def paginated_reports(
    page: int = 1,
    limit: int = 5,
    db: Session = Depends(get_db)
):

    skip = (page - 1) * limit

    reports = db.query(
        Report
    ).offset(
        skip
    ).limit(
        limit
    ).all()

    return reports

@router.get("/recent")
def recent_reports(
    db: Session = Depends(get_db)
):

    reports = db.query(
        Report
    ).order_by(
        Report.timestamp.desc()
    ).limit(
        5
    ).all()

    return reports

@router.get("/top-stations")
def top_stations(
    db: Session = Depends(get_db)
):

    data = db.query(
        Report.station_name,
        func.count(Report.id)
    ).group_by(
        Report.station_name
    ).order_by(
        func.count(
            Report.id
        ).desc()
    ).limit(
        5
    ).all()

    result = []

    for station, count in data:

        result.append(
            {
                "station_name": station,
                "report_count": count
            }
        )

    return result