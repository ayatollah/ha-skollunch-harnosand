"""Konstanter för Skollunch-integrationen."""
from datetime import timedelta

DOMAIN = "skollunch"
SCAN_INTERVAL = timedelta(hours=1)
BASE_URL = "https://skollunch.supergott.com/api/lunch"