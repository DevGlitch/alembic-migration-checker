# Alembic Migration Checker - GitHub Action

![Python Version](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Docker Base Image](https://img.shields.io/badge/Docker%20Image-3.12--slim-blue?logo=docker&logoColor=white)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000?logo=python&logoColor=white)
![License](https://img.shields.io/github/license/DevGlitch/alembic-version-checker?logo=github&logoColor=white&label=License)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/DevGlitch/alembic-version-checker?logo=github&logoColor=white&label=Version)

## 📖 Description

The **Alembic Migration Checker** GitHub Action performs a comprehensive check to ensure that the Alembic version 
recorded in your database aligns with the version of the latest migration script in your Alembic migrations 
directory. It is designed to verify that migrations have been applied in the correct sequence, 
ensuring that the versioning history is intact. This proactive approach helps prevent migration conflicts and
inconsistencies, ensuring a smooth deployment pipeline. By integrating this action into GitHub workflows,
teams can maintain a consistent and accurate reflection of their database migrations, facilitating smoother and
more reliable application deployments, particularly in CI/CD environments.

---

## ⌨️ Inputs

This action supports various inputs to accommodate different database configurations.

_Note that some inputs are not required for all database types, such as SQLite._

- `db_url`: The url of database to check. Alternative to `db_host`, `db_port`, `db_user`, `db_password`, and `db_name`.
- `db_type`: The database type. Supported values are `postgresql`, `mysql`, and `sqlite`. Default: `postgresql`.
- `db_host`: The database host address.
- `db_port`: The database port. Defaults to `5432`.
- `db_user`: The username for database access.
- `db_password`: The password for database access.
- `db_name`: The name of the database to check.
- `alembic_version_table_schema`: The database schema containing the alembic_version table. Defaults to `public`
- `migrations_path`: The path to your Alembic migrations folder. Defaults to `./migrations/`.

___

### 🚦 Exit Status

- **Exit Code 0**: This code indicates successful execution of the action. It can signify one of two scenarios:
    1. No new migrations were detected, and the database schema is fully aligned with the latest migration script.
    2. One or more new migrations were detected, but the database schema is already aligned with the latest migration
       script. In other words, the down revisions of the database match those of the migration scripts, ensuring
       consistency.

- **Exit Code 1**: This code indicates errors or discrepancies encountered during execution. It typically signifies
  that:
    - The database schema does not align with the migration history, indicating potential issues such as missing or
      mismatched migrations. This could require further investigation and corrective action to ensure database
      consistency.

---

## 🛠 Usage

Below are usage examples on how to use the Alembic Migration Checker for different types of supported databases within
your GitHub Actions workflows.

### 🐘 PostgreSQL

You can specify the database connection using either a single connection string (`db_url`) or individual parameters. 
Using `db_url` is convenient when the connection string is available as a single secret.

#### Example Usage with `db_url`:

```yaml
- name: Check Alembic Migration Version
  uses: DevGlitch/alembic-migration-checker@v1.1
  with:
    db_url: ${{ secrets.DB_URL }}  # Format: postgresql+psycopg2://user:password@host:port/dbname
    migrations_path: ./migrations/
```

#### Example Usage with Individual Parameters:

If you prefer, you can specify individual parameters for the database connection. Please note that `db_type` defaults to 
`postgresql`, so it is not necessary to specify it. Also, `db_port` defaults to `5432`, so specify `db_port` only if you are 
using a different port.

```yaml
- name: Check Alembic Migration Version
  uses: DevGlitch/alembic-migration-checker@v1.1
  with:
    db_host: ${{ secrets.DB_HOST }}
    db_port: ${{ secrets.DB_PORT }}  # Only if not using the default port 5432
    db_user: ${{ secrets.DB_USER }}
    db_password: ${{ secrets.DB_PASSWORD }}
    db_name: ${{ secrets.DB_NAME }}
    alembic_version_table_schema: ${{ secrets.ALEMBIC_VERSION_TABLE_SCHEMA }}
    migrations_path: ./migrations/
```

### 🐬 MySQL

When working with MySQL, set the `db_type` to `mysql`. You can specify the database connection using either a single 
connection string (`db_url`) or individual parameters.

#### Example Usage with `db_url`:

```yaml
- name: Check Alembic Migration Version
  uses: DevGlitch/alembic-migration-checker@v1.1
  with:
    db_url: ${{ secrets.DB_URL }}  # Format: mysql://user:password@host:port/dbname
    migrations_path: ./migrations/
```

#### Example Usage with Individual Parameters:

If you prefer, you can specify individual parameters for the database connection.

```yaml
- name: Check Alembic Migration Version
  uses: DevGlitch/alembic-migration-checker@v1.1
  with:
    db_type: mysql
    db_host: ${{ secrets.DB_HOST }}
    db_port: ${{ secrets.DB_PORT }}
    db_user: ${{ secrets.DB_USER }}
    db_password: ${{ secrets.DB_PASSWORD }}
    db_name: ${{ secrets.DB_NAME }}
    migrations_path: ./migrations/
```

### 🪶 SQLite

For SQLite databases, you can either use a `db_url` to specify the entire database connection string or provide individual parameters. When using individual parameters, set the `db_type` to `sqlite`. Note that `db_host`, `db_port`, `db_user`, and `db_password` are not needed for SQLite.

#### Example Usage with `db_url`:

```yaml
- name: Check Alembic Migration Version
  uses: DevGlitch/alembic-migration-checker@v1.1
  with:
    db_url: ${{ secrets.DB_URL }}  # Format: sqlite:///path_to_db_file
    migrations_path: ./migrations/
```

#### Example Usage with Individual Parameters:

```yaml
- name: Check Alembic Migration Version
  uses: DevGlitch/alembic-migration-checker@v1.1
  with:
    db_type: sqlite
    db_name: ${{ secrets.DB_NAME }}  # Path to the SQLite database file
    migrations_path: ./migrations/
```

Ensure that your workflow is correctly set up to use these configurations, adjusting parameters as necessary for your
specific database setup.

---

## 💡 Recommended Use Cases

The **Alembic Migration Checker** GitHub Action is a versatile tool designed to enhance your CI/CD pipeline by providing
essential checks at critical stages of development and deployment. Below are detailed examples of how to integrate this
action into workflows for pull requests and deployments, ensuring database migrations are always synchronized with your
application's expected state.

### 🔀 Pull Requests (PRs)

Integrating the Alembic Migration Checker into the PR review process ensures compatibility between new migrations and
the
existing database schema. This proactive measure helps prevent migration conflicts from affecting the main branch,
promoting stability throughout the development lifecycle.

Here's an example workflow for pull requests:

```yaml
name: Alembic Migration Check on PR

on: pull_request

jobs:
  check-migration:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Check Alembic Migration Version
        uses: DevGlitch/alembic-migration-checker@v1.1
        with:
          db_host: ${{ secrets.DB_HOST }}
          db_name: ${{ secrets.DB_NAME }}
          # Specify other necessary inputs...
```

### 🚀 Deployment Workflows

Before proceeding with deployments to staging or production, employing the Alembic Migration Checker ensures the
database
schema aligns with the repository's migration scripts. This validation lays a solid foundation for application
deployments, mitigating risks associated with schema discrepancies.

An example workflow for deployment might look like this:

```yaml
name: Pre-deployment Alembic Migration Check

on:
  push:
    branches:
      - main

jobs:
  pre-deploy-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Check Alembic Migration Version
        uses: DevGlitch/alembic-migration-checker@v1.1
        with:
          db_host: ${{ secrets.STAGING_DB_HOST }}
          db_name: ${{ secrets.STAGING_DB_NAME }}
          # Include additional inputs as needed...
```

By incorporating the Alembic Migration Checker into these critical workflow stages, teams can significantly enhance the
reliability of their development and deployment processes. This action serves as a safeguard, ensuring that the database
schema is consistently in sync with the application's migration history, thereby facilitating smoother and more
dependable application releases.

---

## 🚨 Error Handling and Troubleshooting

If you encounter any errors or issues while using the Alembic Migration Checker GitHub Action, here are some steps you
can take to troubleshoot:

1. **Check Action Output**: Review the output of the action in your GitHub Actions workflow runs to identify any error
   messages or unexpected behavior.
2. **Review Configuration**: Double-check the configuration inputs provided to the action in your workflow file to
   ensure they are correctly specified.
3. **Inspect Database Connection**: Verify that the database connection details (host, port, username, password, etc.)
   are accurate and allow access to the specified database.
4. **Check Migration History**: Examine the Alembic migration history and scripts to identify any discrepancies or
   issues that may be causing the action to fail.
5. **Open an Issue**: If you are unable to resolve the issue on your own, please open an issue in the GitHub repository
   with details about the problem you're experiencing. This will allow the maintainers to assist you and address any
   underlying issues.

By following these steps, you can effectively troubleshoot and resolve any errors encountered while using the Alembic
Migration Checker GitHub Action.

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

You are welcome to contribute to this project by submitting a pull request. If you have any suggestions or problems,
please open an issue. Thank you!

---

## 💖 Support

Your support keeps this project going!

- ⭐️ **Star**: Show your appreciation by giving this project a star.
- ☕️ **[Buy Me a Coffee](https://github.com/sponsors/DevGlitch)**: Contribute by buying a virtual coffee.
- 💼 **[Sponsor This Project](https://github.com/sponsors/DevGlitch)**: Consider sponsoring for ongoing support.

Making a difference, one line of code at a time...
