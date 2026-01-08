import os
from pathlib import Path

import psycopg


def load_statements(path: Path) -> list[str]:
    raw_sql = path.read_text(encoding="utf-8")
    return [stmt.strip() for stmt in raw_sql.split(";") if stmt.strip()]


def main() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL environment variable is not set")

    migrations_dir = Path(__file__).resolve().parent.parent / "migrations"
    migration_path = migrations_dir / "0001_init.sql"
    statements = load_statements(migration_path)

    if not statements:
        raise SystemExit(f"No SQL statements found in {migration_path}")

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            for statement in statements:
                cur.execute(statement)

    print(f"Applied {migration_path.name}")


if __name__ == "__main__":
    main()
