from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
db_url = "postgresql://postgres:root@localhost:5432/inventorydb"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)