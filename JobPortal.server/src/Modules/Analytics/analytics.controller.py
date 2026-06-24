from sqlalchemy.orm import Session
from src.Modules.Analytics.service import AnalyticsService

class AnalyticsController:
    @staticmethod
    def get_summary(db: Session):
        return AnalyticsService.get_analytics_summary(db)
