from pydantic import BaseModel, SecretStr, fields
from pydantic_settings import SettingsConfigDict


class AppSettings(BaseModel):
    debug_mode: bool = fields.Field(alias='DEBUG_MODE', default=True)
    secret_key: SecretStr = fields.Field(alias='SECRET_KEY')

class DataBaseSettings(BaseModel):
    db_engine: str = fields.Field(alias='DB_ENGINE')
    db_name: SecretStr = fields.Field(alias='DB_NAME')
    db_user: str = fields.Field(alias='DB_USER')
    db_host: str = fields.Field(alias='DB_HOST')
    db_port: str = fields.Field(alias='DB_PORT')
    db_password: SecretStr = fields.Field(alias='DB_PASSWORD')



class Settings(
    AppSettings,
    DataBaseSettings,
):
    model_config = SettingsConfigDict(extra='ignore')
