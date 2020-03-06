import time
from .models import Probes, DataEntries

"""
Sentry is a service that polls sensors configured through the webapp for data
"""

while True:
  