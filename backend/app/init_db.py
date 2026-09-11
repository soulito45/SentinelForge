from backend.app.database import Base, engine
from backend.app.models import Domain, Asset, Scan, IPAddress


def init_db():
    Base.metadata.create_all(bind=engine)
    print("RYNEX database tables created successfully.")


if __name__ == "__main__":
    init_db()
