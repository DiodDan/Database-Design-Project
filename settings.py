from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings

DOTENV = Path(__file__).parent / ".env"


class Settings(BaseSettings, extra="allow"):
    # Postgres
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    PG_PORT: int
    PG_HOST: str
    PG_DSN: str = ""

    # Postgres Admin
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str
    PGADMIN_LISTEN_PORT: int

    @model_validator(mode="after")  # type: ignore
    def setup_pg_dsn(self) -> None:
        self.PG_DSN: str = (  # pylint: disable=invalid-name
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            + f"{self.PG_HOST}:{self.PG_PORT}/{self.POSTGRES_DB}"
        )


settings: Settings = Settings(_env_file=DOTENV)
