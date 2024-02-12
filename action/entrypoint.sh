#!/bin/sh

python /check_alembic_version.py "${DB_TYPE}" "${DB_HOST}" "${DB_PORT}" "${DB_USER}" "${DB_PASSWORD}" "${DB_NAME}" "${MIGRATIONS_PATH}"
