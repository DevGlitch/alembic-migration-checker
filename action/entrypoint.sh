#!/bin/sh -l

python /check_alembic_migration.py --db_url="${INPUT_DB_URL}" --db_type="${INPUT_DB_TYPE}" --db_host="${INPUT_DB_HOST}" --db_port="${INPUT_DB_PORT}" --db_user="${INPUT_DB_USER}" --db_password="${INPUT_DB_PASSWORD}" --db_name="${INPUT_DB_NAME}" --alembic_version_table_schema="${INPUT_ALEMBIC_VERSION_TABLE_SCHEMA}" --migrations_path="${INPUT_MIGRATIONS_PATH}"
