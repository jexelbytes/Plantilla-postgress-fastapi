from seeders.seeder import init_s
from database import SessionLocal

db = SessionLocal()
init_s(db=db)
db.close()