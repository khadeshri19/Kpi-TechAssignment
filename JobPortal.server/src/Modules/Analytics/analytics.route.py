from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.dependencies import RoleChecker
from src.models import UserRole
from src.Modules.Analytics.types import AnalyticsSummaryResponse
from src.Modules.Analytics.controller import AnalyticsController

router = APIRouter(prefix="/analytics", tags=["Analytics"])

admin_guard = RoleChecker([UserRole.admin])

@router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_summary(
    db: Session = Depends(get_db),
    _current_user = Depends(admin_guard)
):
    """
    Retrieves system analytics summary. Accessible by Administrators only.
    """
    return AnalyticsController.get_summary(db)
