
from django.conf import settings
import pandas as pd
import requests

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from core.models import (Client, Consumers)



