FROM python:3.12-slim

# set the working dir to /src
WORKDIR /src

# install dependencies first
COPY services/persistence-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy of config for tracer and logger
COPY services/config ./services/config
# copy the persistence_service folder and everything else to /src
COPY services/persistence-service/persistence_service/ ./persistence_service/

# set path
ENV PYTHONPATH=/src

# run the service
CMD ["python", "-m", "persistence_service.canonical_events_consumer"]