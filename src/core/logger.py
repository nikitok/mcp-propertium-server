import logging
import sys

def setup_logging():
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
