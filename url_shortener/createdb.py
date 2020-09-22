import os
import sys
sys.path.append(os.getcwd())

from url_shortener import create_app
from url_shortener.extensions import db, ma
from url_shortener.models import Link

db.create_all(app=create_app())

# Нужно создать БД