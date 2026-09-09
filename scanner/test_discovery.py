from backend.app.database import SessionLocal
from backend.app.models import Domain
from scanner.discovery_pipeline import run_discovery


db = SessionLocal()

try:
    domain = db.query(Domain).first()

    if domain is None:
        raise RuntimeError(
            "No domain exists in the database."
        )

    count = run_discovery(
        db=db,
        domain_id=domain.id,
        domain_name=domain.name,
    )

    print()
    print("========== DISCOVERY RESULT ==========")
    print("Domain:", domain.name)
    print("Assets processed:", count)

finally:
    db.close()
