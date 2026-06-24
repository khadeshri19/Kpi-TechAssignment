from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.dependencies import RoleChecker
from src.models import UserRole
from src.Modules.Dashboard.types import DashboardMetricsResponse
from src.Modules.Dashboard.controller import DashboardController

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

admin_guard = RoleChecker([UserRole.admin])

@router.get("/metrics", response_model=DashboardMetricsResponse)
def get_metrics(
    db: Session = Depends(get_db),
    _current_user = Depends(admin_guard)
):
    """
    Retrieves system analytics metrics. Accessible by Administrators only.
    """
    return DashboardController.get_metrics(db)
