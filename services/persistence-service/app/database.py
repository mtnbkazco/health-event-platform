from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker
from app.models.fhir_resource_model import FhirResource
from services.config.logger_config import get_logger


class Database:
    def __init__(self, connection_url):
        # Initialize a pool for efficiency
        self.engine = create_engine(
            connection_url,
            pool_size=2,
            max_overflow=10,
            pool_pre_ping=True
        )
        self.Session = sessionmaker(bind=self.engine)
        self.logger = get_logger("database-service")

        self.logger.info("Database connection pool initialized")

    def save_resource(self, resource_type, data, trace_id):
        session = self.Session()
        try:
            values = {
                "trace_id": trace_id,
                "source": data.get("source"),
                "tenant_id": data.get("tenantId"),
                "event_type": data.get("eventType"),
                "original_event_type": data.get("originalEventType"),
                "resource_type": resource_type,
                "fhir_id": data.get('data').get("id"),
                "data": data
            }
            statement = insert(FhirResource).values(**values)
            # if fhir_id already exists update data and trace_id
            statement = statement.on_conflict_do_update(
                index_elements=['fhir_id'],
                set_={
                    "data": values["data"],
                    "trace_id": values["trace_id"]
                }
            )
            session.execute(statement)
            session.commit()
            self.logger.info(
                f"Successfully upserted resource: {values['fhir_id']}",
                extra={
                    "event_id": data.get("eventId"),
                    "tenant": data.get("tenantId"),
                    "trace_id": trace_id
                }
            )

        except Exception as e:
            session.rollback()
            self.logger.error(f"DB SAVE ERROR: {e}")
            raise
        finally:
            session.close()

    def close_connection(self):
        session = self.Session()
        session.close()
        self.logger.info("Database connections closed")

    def disconnect(self):
        """Call this ONLY when the service is stopping"""
        self.engine.dispose()
        self.logger.info("Database connection pool disposed.")