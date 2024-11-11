from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_HOST: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_EXPIRE_TIME: int = 1200  # 20 minutes
    REFRESH_EXPIRE_TIME: int = 86400  # 1 day

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}/{self.POSTGRES_DB}"
        )

    @property
    def postgres_test_url(self) -> str:
        return (
            f"postgresql://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}@"
            f"{self.TEST_POSTGRES_HOST}/{self.TEST_POSTGRES_DB}"
        )


settings = Settings()
