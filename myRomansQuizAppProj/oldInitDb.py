# init_db.py
from models import init_db
from models import Base, engine, Session, Question

def init_db():
    Base.metadata.create_all(engine)
    print("✅ PostgreSQL tables created.")

if __name__ == "__main__":
    init_db()

