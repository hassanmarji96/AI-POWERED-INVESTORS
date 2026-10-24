# import os
# from urllib.parse import quote
#
# import psycopg2
# from dotenv import load_dotenv
# from sqlalchemy import create_engine, text
#
# load_dotenv()
#
#
# class MissingPostgresConfigError(RuntimeError):
#     """Sollevata quando mancano variabili d'ambiente PostgreSQL obbligatorie."""
#
#     def __init__(self, missing: list[str]) -> None:
#         self.missing = missing
#         super().__init__(
#             "Configurazione PostgreSQL incompleta. "
#             f"Variabili mancanti nel file .env: {', '.join(missing)}"
#         )
#
#
# def _require_postgres_env() -> dict[str, str]:
#     names = ["POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_USER", "POSTGRES_PASSWORD"]
#     values = {name: os.getenv(name) for name in names}
#     missing = [name for name, value in values.items() if not value]
#     if missing:
#         raise MissingPostgresConfigError(missing)
#     return values  # type: ignore[return-value]
#
#
# def get_engine(database: str | None = None):
#     """
#     Create PostgreSQL connection.
#
#     Args:
#         database: Database name. Defaults to POSTGRES_DATABASE from .env.
#     """
#     if database is None:
#         database = os.getenv("POSTGRES_DATABASE")
#
#     config = _require_postgres_env()
#     if not database:
#         raise MissingPostgresConfigError(["POSTGRES_DATABASE"])
#
#     host = config["POSTGRES_HOST"]
#     port = config["POSTGRES_PORT"]
#     user = config["POSTGRES_USER"]
#     password = config["POSTGRES_PASSWORD"]
#
#     # URL-encode credentials to handle special characters (e.g., @ in password)
#     encoded_user = quote(user, safe="")
#     encoded_password = quote(password, safe="")
#
#     connection_string = (
#         f"postgresql+psycopg2://"
#         f"{encoded_user}:{encoded_password}@{host}:{port}/{database}"
#         "?sslmode=require"
#     )
#
#     return create_engine(connection_string)


# def create_database() -> None:
#     """
#     Create the target database if it does not exist.
#
#     Uses psycopg2 directly with autocommit to bypass SQLAlchemy transaction wrapping.
#     """
#     target_db = os.getenv("POSTGRES_DATABASE")
#     host = os.getenv("POSTGRES_HOST")
#     port = os.getenv("POSTGRES_PORT")
#     user = os.getenv("POSTGRES_USER")
#     password = os.getenv("POSTGRES_PASSWORD")
#
#     try:
#         # Connect to default 'postgres' database using psycopg2 directly
#         conn = psycopg2.connect(
#             host=host,
#             port=port,
#             database="postgres",
#             user=user,
#             password=password,
#             sslmode="require"
#         )
#         # Enable autocommit mode before executing CREATE DATABASE
#         conn.autocommit = True
#
#         cursor = conn.cursor()
#         try:
#             # Check if database exists
#             cursor.execute(
#                 "SELECT 1 FROM pg_database WHERE datname = %s",
#                 (target_db,)
#             )
#
#             if not cursor.fetchone():
#                 print(f"Database '{target_db}' does not exist. Creating...")
#                 cursor.execute(f"CREATE DATABASE {target_db}")
#                 print(f"Database '{target_db}' created successfully.")
#             else:
#                 print(f"Database '{target_db}' already exists.")
#         finally:
#             cursor.close()
#             conn.close()
#     except Exception as exc:
#         print(f"Failed to create database: {exc}")
#         raise