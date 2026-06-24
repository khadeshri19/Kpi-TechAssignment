import logging
import sys

def setup_logger():
    """
    Configures a standard logger for the application.
    """
    app_logger = logging.getLogger("job_board")
    app_logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers if setup multiple times
    if not app_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        )
        handler.setFormatter(formatter)
        app_logger.addHandler(handler)
    return app_logger

logger = setup_logger()
