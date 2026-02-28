\"\"\"Configuration for River Rule service.\"\"\"
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "River Rule"
    river_rule_version: str = "v1.0.0"

    class Config:
        env_file = ".env"


settings = Settings()
