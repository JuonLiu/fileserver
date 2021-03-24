import logging
import os

import sys

from src.logger import SafeFileHandler
from src.settings import LOG_FILE_PATH

rf_handler = logging.StreamHandler(sys.stderr)  # 默认是sys.stderr
rf_handler.setLevel(logging.DEBUG)
log_file_handler = SafeFileHandler(filename=os.path.join(LOG_FILE_PATH, 'all.log'))
err_log_file_handler = SafeFileHandler(filename=os.path.join(LOG_FILE_PATH, 'critical.log'))
err_log_file_handler.setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                    handlers=[rf_handler, log_file_handler, err_log_file_handler])

logger = logging.getLogger(__name__)
