from sqlalchemy.orm import Session
from src.Modules.Dashboard.service import DashboardService

class DashboardController:
    @staticmethod
    def get_metrics(db: Session):
        return DashboardService.get_dashboard_metrics(db)
