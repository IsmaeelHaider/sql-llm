import os
from langchain import SQLDatabase

from dotenv import load_dotenv

load_dotenv()

db = SQLDatabase.from_uri(os.getenv('POSTGRES_URI'))

db_schema = db.table_info