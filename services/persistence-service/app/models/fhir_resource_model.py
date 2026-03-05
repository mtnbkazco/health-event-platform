from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    # required for setup
    pass


class FhirResource(Base):
    __tablename__ = "fhir_resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String(100), index=True)
    source = Column(String(48))
    tenant_id = Column(String(48))
    event_type = Column(String(48))
    original_event_type = Column(String(48))
    resource_type = Column(String(48), nullable=False)
    fhir_id = Column(String(100), unique=True, index=True)  # id field inside resource
    data = Column(JSONB, nullable=False)  # full resource
    created_at = Column(DateTime, server_default=func.now())
