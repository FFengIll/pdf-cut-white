import sys

import loguru

logger = loguru.logger
logger.remove()
logger.add(sys.stderr, level="INFO")
