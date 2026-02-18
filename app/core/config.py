from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "AI Trafik Polisi"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./traffic_police.db"


settings = Settings()
