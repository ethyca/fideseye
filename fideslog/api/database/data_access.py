from json import dumps
from logging import getLogger

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from fideslog.api.database.models import AnalyticsEvent as AnalyticsEventORM
from fideslog.api.models.analytics_event import AnalyticsEvent

log = getLogger(__name__)


def create_event(database: Session, event: AnalyticsEvent) -> None:
    """Create a new analytics event."""

    try:
        log.debug("Creating resource")
        extra_data = dumps(event.extra_data) if event.extra_data else None
        flags = ", ".join(event.flags) if event.flags else None
        resource_counts = (
            dumps(event.resource_counts.dict()) if event.resource_counts else None
        )
        database.add(
            AnalyticsEventORM(
                client_id=event.client_id,
                command=event.command,
                developer=event.developer,
                docker=event.docker,
                endpoint=event.endpoint,
                error=event.error,
                event=event.event,
                event_created_at=event.event_created_at,
                extra_data=extra_data,
                flags=flags,
                local_host=event.local_host,
                os=event.os,
                product_name=event.product_name,
                production_version=event.production_version,
                resource_counts=resource_counts,
                status_code=event.status_code,
            )
        )
        database.commit()
    except DBAPIError:
        log.error("Insert Failed")
