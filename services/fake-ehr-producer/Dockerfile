FROM python:3.12-slim

# set the working dir to /src
WORKDIR /src

# install dependencies first
COPY services/fake-ehr-producer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy of config for tracer and logger
COPY services/config ./services/config

# copy the fake_ehr_producer folder and everything else to /src
COPY services/fake-ehr-producer/fake_ehr_producer/ ./fake_ehr_producer/

# run the service
CMD ["python", "-m", "fake_ehr_producer.ehr_producer"]