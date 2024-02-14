#!/bin/sh -l

python /check_alembic_migration.py "${INPUT_DB_TYPE}" "${INPUT_DB_HOST}" "${INPUT_DB_PORT}" "${INPUT_DB_USER}" "${INPUT_DB_PASSWORD}" "${INPUT_DB_NAME}" "${INPUT_MIGRATIONS_PATH}"
