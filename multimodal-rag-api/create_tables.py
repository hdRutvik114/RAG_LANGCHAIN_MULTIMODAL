from app.core.database import Base, engine
from app.models import Document

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
print("Registered tables:", list(Base.metadata.tables.keys()))