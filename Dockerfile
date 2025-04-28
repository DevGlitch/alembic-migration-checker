FROM python:3.12-slim

# Install dependencies
RUN pip install sqlalchemy
RUN pip install alembic
RUN pip install sqlmodel
RUN pip install psycopg2-binary

# Install mysqlclient and its debian package dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb-dev-compat gcc                   `: MySQL client` \
    && rm -rf /var/lib/apt/lists/*\
RUN pip install mysqlclient

# Copy files from the action folder to the root in the Docker image
COPY action/entrypoint.sh /entrypoint.sh
COPY action/check_alembic_migration.py /check_alembic_migration.py

# Ensure entrypoint.sh is executable
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
