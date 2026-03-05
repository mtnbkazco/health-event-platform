FROM python:3.12-slim

# set the working dir to /src
WORKDIR /src

# install dependencies first
COPY services/normalization-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p services/config
# copy of config for tracer and logger
COPY services/config ./services/config

# copy the normalization_service folder and everything else to /src
COPY services/normalization-service/normalization_service/ ./normalization_service/

# set path
ENV PYTHONPATH=/src

# run the service
CMD ["python", "-m", "normalization_service.normalize_events_consumer"]