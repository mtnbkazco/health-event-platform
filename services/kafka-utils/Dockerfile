FROM python:3.12-slim

WORKDIR /src

# Install only what the migrator needs
RUN pip install --no-cache-dir confluent-kafka pyyaml

# Copy the script and the topics config
COPY services/kafka-utils/ ./app/

# set path
ENV PYTHONPATH=/src

# Run the script directly
CMD ["python", "app/topics_migration"]
