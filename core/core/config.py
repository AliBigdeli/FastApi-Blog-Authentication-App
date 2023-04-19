from pydantic import BaseSettings

class Settings(BaseSettings):
    
    # postgres envs
    
    PGDB_USERNAME: str
    PGDB_PASSWORD: str
    PGDB_PORT: int
    PGDB_DBNAME: str
    PGDB_HOSTNAME: str
    
    # mongo envs
    # MGDB_USERNAME: str
    # MGDB_PASSWORD: str
    # MGDB_PORT: int
    # MGDB_DBNAME: str
    # MGDB_HOSTNAME: str
    
    # Sentry debugger
    ENABLE_SENTRY:bool
    SENTRY_DSN:str


settings = Settings()