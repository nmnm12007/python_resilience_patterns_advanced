"""
    Observability Logging
"""

import logging

logger = logging.getLogger("resilience_full_impl")

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | '
                                  '%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
logger.setLevel(logging.INFO)

