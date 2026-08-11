from __future__ import annotations

import os

import psycopg
from psycopg import sql

ROLE_NAME = "dtmo_grafana_reader"
REPORTING_SCHEMA = "dtmo_reporting"
REQUIRED_VIEWS = ("intelligence_items_safe", "connector_health_safe")


def _dsn() -> str:
    value = os.environ.get("DTMO_DATABASE_URL", "").strip()
    if not value:
        raise RuntimeError("DTMO_DATABASE_URL is required")
    return value.replace("postgresql+psycopg://", "postgresql://", 1)


def _password() -> str:
    value = os.environ.get("GRAFANA_DB_PASSWORD", "")
    if len(value) < 20:
        raise RuntimeError("GRAFANA_DB_PASSWORD must be at least 20 characters")
    return value


def provision() -> None:
    password = _password()
    with psycopg.connect(_dsn(), autocommit=True) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database()")
            database = str(cursor.fetchone()[0])
            cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (ROLE_NAME,))
            exists = cursor.fetchone() is not None
            role = sql.Identifier(ROLE_NAME)
            password_literal = sql.Literal(password)
            if exists:
                cursor.execute(
                    sql.SQL(
                        "ALTER ROLE {} WITH LOGIN PASSWORD {} NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION"
                    ).format(role, password_literal)
                )
            else:
                cursor.execute(
                    sql.SQL(
                        "CREATE ROLE {} WITH LOGIN PASSWORD {} NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION"
                    ).format(role, password_literal)
                )

            cursor.execute(sql.SQL("REVOKE ALL ON SCHEMA public FROM {}").format(role))
            cursor.execute(
                sql.SQL("GRANT CONNECT ON DATABASE {} TO {}").format(
                    sql.Identifier(database), role
                )
            )
            cursor.execute(
                sql.SQL("GRANT USAGE ON SCHEMA {} TO {}").format(
                    sql.Identifier(REPORTING_SCHEMA), role
                )
            )
            for view_name in REQUIRED_VIEWS:
                cursor.execute(
                    sql.SQL("GRANT SELECT ON {}.{} TO {}").format(
                        sql.Identifier(REPORTING_SCHEMA),
                        sql.Identifier(view_name),
                        role,
                    )
                )


if __name__ == "__main__":
    provision()
