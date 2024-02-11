# Alembic Version Checker - GitHub Action

![Python Version](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Docker Base Image](https://img.shields.io/badge/Docker%20Image-3.12--slim-blue?logo=docker&logoColor=white)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000?logo=python&logoColor=white)
![License](https://img.shields.io/github/license/DevGlitch/Alembic_Version_Checker?logo=github&logoColor=white&label=License)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/DevGlitch/Alembic_Version_Checker?logo=github&logoColor=white&label=Version)

## 📖 Description

The **Alembic Version Checker** GitHub Action checks the Alembic version of the latest migration against the database.
It supports PostgreSQL, MySQL, and SQLite databases, making it versatile for different development environments.

This GitHub action automates a critical aspect of database schema migrations management. It employs a custom Python
script that connects directly to your database and queries the `alembic_version` table for the version number of the
currently applied migration. This number is then compared with the version identifier of the latest migration script
available in your Alembic migrations directory.

The primary aim is to detect any discrepancies between the applied database migration and the latest migration script,
preventing potential conflicts or inconsistencies before they impact your deployment pipeline. By incorporating this
check into GitHub workflows, teams can maintain a consistent and accurate reflection of their database migrations,
facilitating smoother and more reliable application deployments especially in CI/CD environments.

---

## ⌨️ Inputs

This action supports various inputs to accommodate different database configurations.

_Note that some inputs are not required for all database types, such as SQLite._

- `db_type`: Specifies the type of database. Supported values are `postgresql`, `mysql`, and `sqlite`.
  Default: `postgresql`.
- `db_host`: The database host address.
- `db_port`: The database port. Defaults to `5432`.
- `db_user`: The username for database access.
- `db_password`: The password for database access.
- `db_name`: The name of the database to check.
- `migrations_path`: The path to your Alembic migrations folder. Defaults to `migrations/versions`.

___

## 🛠 Usage

Below are usage examples on how to use the Alembic Version Checker for different types of supported databases within
your GitHub Actions workflows.

### 🐘 PostgreSQL Example

Please note that `db_type` is by default `postgresql`. So, for this type of database it is not necessary to specify it.
Also, `db_port` is by default `5432`, specify the `db_port` only if you use a different one.

```yaml
- name: Check Alembic Version
  uses: DevGlitch/alembic-version-checker@v1
  with:
    db_host: ${{ secrets.DB_HOST }}
    db_port: ${{ secrets.DB_PORT }}  # Only if not using 5432 default port
    db_user: ${{ secrets.DB_USER }}
    db_password: ${{ secrets.DB_PASSWORD }}
    db_name: ${{ secrets.DB_NAME }}
    migrations_path: migrations/versions
```

### 🐬 MySQL

When working with MySQL, change the `db_type` to `mysql`. This example includes all necessary parameters for a MySQL
database connection.

```yaml
- name: Check Alembic Version
  uses: DevGlitch/alembic-version-checker@v1
  with:
    db_type: mysql
    db_host: ${{ secrets.DB_HOST }}
    db_port: ${{ secrets.DB_PORT }}
    db_user: ${{ secrets.DB_USER }}
    db_password: ${{ secrets.DB_PASSWORD }}
    db_name: ${{ secrets.DB_NAME }}
    migrations_path: migrations/versions
```

### 🪶 SQLite

For SQLite databases, change the `db_type` to `sqlite`. The configuration is simplified
as `db_host`, `db_port`, `db_user`, and `db_password` are not needed.

```yaml
- name: Check Alembic Version
  uses: DevGlitch/alembic-version-checker@v1
  with:
    db_type: sqlite
    db_name: ${{ secrets.DB_NAME }}
    migrations_path: migrations/versions
```

Ensure that your workflow is correctly set up to use these configurations, adjusting parameters as necessary for your
specific database setup.

---

## 💡 Recommended Use Cases

The **Alembic Version Checker** GitHub Action is a versatile tool designed to enhance your CI/CD pipeline by providing
essential checks at critical stages of development and deployment. Below are detailed examples of how to integrate this
action into workflows for pull requests and deployments, ensuring database migrations are always synchronized with your
application's expected state.

### 🔀 Pull Requests (PRs)

Integrating the Alembic Version Checker into the PR review process ensures compatibility between new migrations and the
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
        uses: DevGlitch/alembic-version-checker@v1
        with:
          db_host: ${{ secrets.DB_HOST }}
          db_name: ${{ secrets.DB_NAME }}
          # Specify other necessary inputs...
```

### 🚀 Deployment Workflows

Before proceeding with deployments to staging or production, employing the Alembic Version Checker ensures the database
schema aligns with the repository's migration scripts. This validation lays a solid foundation for application
deployments, mitigating risks associated with schema discrepancies.

An example workflow for deployment might look like this:

```yaml
name: Pre-deployment Alembic Check

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

      - name: Alembic Migration Version Check
        uses: your-username/alembic-version-checker@v1
        with:
          db_host: ${{ secrets.STAGING_DB_HOST }}
          db_name: ${{ secrets.STAGING_DB_NAME }}
          # Include additional inputs as needed...
```

By incorporating the Alembic Version Checker into these critical workflow stages, teams can significantly enhance the
reliability of their development and deployment processes. This action serves as a safeguard, ensuring that the database
schema is consistently in sync with the application's migration history, thereby facilitating smoother and more
dependable application releases.

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

You are welcome to contribute to this project by submitting a pull request. If you have any suggestions or problems, please open an issue. Thank you!

---

## 💖 Support

Your support keeps this project going!

- ⭐️ **Star**: Show your appreciation by giving this project a star.
- ☕️ **[Buy Me a Coffee](https://github.com/sponsors/DevGlitch)**: Contribute by buying a virtual coffee.
- 💼 **[Sponsor This Project](https://github.com/sponsors/DevGlitch)**: Consider sponsoring for ongoing support.



Making a difference, one line of code at a time...
