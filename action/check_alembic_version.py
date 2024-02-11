"""
This script checks the Alembic version of the latest migration against the database.
It supports PostgreSQL, MySQL, and SQLite databases.
"""

import os
import sys

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, MetaData
from sqlalchemy.sql import select


class AlembicVersionChecker:
    """A class to check the Alembic migration version against the database version."""

    def __init__(
        self, db_type, db_host, db_port, db_user, db_password, db_name, migrations_path
    ):
        """
        Initializes the AlembicVersionChecker with database connection details and migrations folder path.

        :param db_type: The database type (postgresql, mysql, sqlite)
        :param db_host: The database host address
        :param db_port: The database port
        :param db_user: The database user
        :param db_password: The database password
        :param db_name: The database name
        :param migrations_path: The path to Alembic migrations folder
        """
        print("Initializing AlembicVersionChecker...")
        self.db_type = db_type
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.migrations_path = migrations_path

        self.db_url = self._get_database_url()
        self.engine = create_engine(self.db_url)

        validation_error = self._validate_inputs()
        if validation_error:
            raise ValueError(validation_error)

    def _validate_inputs(self):
        """
        Validates the necessary inputs for connecting to a database and accessing the migrations folder path.

        Returns:
            str: An error message string if validation fails, indicating the reason for the failure. Returns None if all validations pass.

        Raises:
            Exception: Catches and returns any exceptions as error messages that occur during the validation of the migrations folder path.

        """
        try:
            # Validate database name
            if not self.db_name:
                return "ERROR: Database name is required."

            # Validate database type
            if self.db_type not in {"postgresql", "mysql", "sqlite"}:
                return "ERROR: Invalid database type. Supported types are 'postgresql', 'mysql', and 'sqlite'."

            # Validate inputs for non-SQLite databases
            if self.db_type != "sqlite" and (
                not self.db_host
                or not self.db_port
                or not self.db_user
                or not self.db_password
            ):
                return "ERROR: Database host, port, user, and password are required for non-SQLite databases."

            # Check migrations path existence
            if not os.path.exists(self.migrations_path):
                print(self.migrations_path)
                return (
                    f"ERROR: Migrations path '{self.migrations_path}' does not exist."
                )

            return None
        except Exception as e:
            # Handle any exceptions that were raised during validation
            return f"Error during input validation: {e}"

    def _get_database_url(self):
        """Constructs and returns the database URL."""
        if self.db_type == "sqlite":
            return f"sqlite:///{self.db_name}"  # SQLite doesn't use port
        else:
            return f"{self.db_type}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    def create_alembic_config(self):
        """Creates a custom Alembic Config object in memory for accessing migration information."""
        alembic_cfg = Config()
        alembic_cfg.set_main_option("script_location", self.migrations_path)
        alembic_cfg.set_main_option("sqlalchemy.url", self.db_url)
        return alembic_cfg

    def get_latest_migration_version(self):
        """Returns the latest migration version from the Alembic migrations directory."""
        print(
            "Retrieving the latest migration version from the Alembic migrations directory..."
        )

        # Assuming self.migrations_path points to the directory containing 'alembic.ini'
        alembic_cfg = Config(os.path.join(self.migrations_path, "alembic.ini"))
        script = ScriptDirectory.from_config(alembic_cfg)

        # Get the head revision, assuming linear migrations without branches for simplicity
        head_revision = script.get_revision("head")
        if head_revision is not None:
            print("Latest migration version found.")
            return head_revision.revision
        else:
            print("ERROR: No head revision found in Alembic migrations.")
            return None

    def get_db_version(self):
        """Fetches and returns the current database version from the Alembic version table."""
        print("Attempting to fetch the current database version...")
        try:
            metadata = MetaData()
            metadata.reflect(bind=self.engine)
            alembic_version_table = metadata.tables["alembic_version"]

            query = select(alembic_version_table.c.version_num).limit(1)

            with self.engine.connect() as connection:
                result = connection.execute(query)
                db_version = result.fetchone()[0]
                print(f"Database version fetched successfully.")
                return db_version
        except Exception as e:
            print("Error fetching database version:", e)
            sys.exit(1)

    def compare_versions(self):
        """
        Compares the latest migration version with the database version.
        Prints the result and exits the script with an error if they don't match.
        """
        print(
            "Comparing version between the latest migration and the database..."
        )
        latest_migration_version = self.get_latest_migration_version()
        db_version = self.get_db_version()
        print(
            f"Latest Alembic migration version (down_revision): {latest_migration_version}"
        )
        print(f"Current Alembic version: {db_version}")

        if latest_migration_version == db_version:
            print(
                "SUCCESS: Version verification passed.\n"
                "The down_revision in the latest Alembic migration script matches the current Alembic version."
            )
            return 0
        else:
            print(
                "ERROR: Version mismatch detected.\n"
                "The down_revision in the latest Alembic migration script doesn't match the current Alembic version.\n"
                "Action Required: Please review your migration scripts."
            )
            sys.exit(1)


def main():
    """The main function of the script."""

    # Check if the correct number of inputs is provided (7 inputs expected)
    if len(sys.argv) - 1 != 7:
        print("Error: Missing required inputs.")
        sys.exit(1)

    # Unpack inputs (excluding the script name) into variables
    (
        db_type,
        db_host,
        db_port,
        db_user,
        db_password,
        db_name,
        migrations_path,
    ) = sys.argv[1:]

    # Initialize the AlembicVersionChecker class with the unpacked inputs
    checker = AlembicVersionChecker(
        db_type, db_host, db_port, db_user, db_password, db_name, migrations_path
    )

    # Call the compare_versions method to compare the latest migration version with the database version
    checker.compare_versions()


if __name__ == "__main__":
    main()
