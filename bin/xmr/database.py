from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import json

# Initiate connection and create session
engine = create_engine('postgresql://xonotic:password@localhost/map_repo')
Base = declarative_base()
session = Session(engine)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)