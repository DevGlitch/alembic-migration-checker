#!/bin/sh -l

python /check_alembic_migration.py "${DB_TYPE}" "${DB_HOST}" "${DB_PORT}" "${DB_USER}" "${DB_PASSWORD}" "${DB_NAME}" "${MIGRATIONS_PATH}"
