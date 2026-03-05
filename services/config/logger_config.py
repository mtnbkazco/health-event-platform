import contextvars
import logging

trace_id = contextvars.ContextVar("trace_id", default="SYSTEM")


class TraceFilter(logging.Filter):
    def filter(self, record):
        # pulling from context
        record.trace_id = trace_id.get()
        # set for EXTRA - must set defaults or formatter will crash
        if not hasattr(record, "event_id"):
            record.event_id = "n/a"
        if not hasattr(record, "tenant"):
            record.tenant = "n/a"
        return True # so the log will show

# create a helper to get pre-config logger
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False  # stop logs from vanishing into the root

    if not logger.handlers: # prevent dups
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | [%(trace_id)s] [%(event_id)s] [%(tenant)s] | %(message)s"
        )
        handler.setFormatter(formatter)
        handler.addFilter(TraceFilter())
        logger.addHandler(handler)

    return logger