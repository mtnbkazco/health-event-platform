FROM python:3.12-slim

# set the working dir to /src
WORKDIR /src

# install dependencies first
COPY services/persistence-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy of config for tracer and logger
COPY services/config ./services/config
# copy the app folder and everything else to /src
COPY services/persistence-service/app/ ./app/

# set path
ENV PYTHONPATH=/src

# run the service
CMD ["python", "-m", "app.canonical_events_consumer"]