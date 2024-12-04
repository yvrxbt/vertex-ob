import logging
import os
from datetime import datetime
from pathlib import Path

class Logger:
    @staticmethod
    def setup_logger(name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # Create logs directory structure
        current_date = datetime.now()
        month_dir = current_date.strftime("%Y%m")
        log_file = current_date.strftime("%Y%m%d.out")
        
        log_dir = Path("logs") / month_dir
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_path = log_dir / log_file
        
        # File handler for all logs
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        
        # Formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d|%(levelname)s|%(name)s|%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(detailed_formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        
        return logger
