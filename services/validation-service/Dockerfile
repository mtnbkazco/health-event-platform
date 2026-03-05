FROM python:3.12-slim

# set the working dir to /src
WORKDIR /src

# install dependencies first
COPY services/validation-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy of config for tracer and logger
COPY services/config ./services/config
# copy the validation and schema folders and everything else to /src
COPY services/validation-service/validation_service/ ./validation_service/

# set path
ENV PYTHONPATH=/src

# run the service
CMD ["python", "-m", "validation_service.raw_events_consumer"]