from pathlib import Path

from pydantic import (
    BaseModel,
    BaseSettings,
    Field,
    validator,
    ValidationError,
    PostgresDsn,
    PositiveInt,
    PositiveFloat,
)


class ApiSettings(BaseModel):
    url: str = 'http://api:8080'


class SourceProcessorSettings(BaseModel):
    url: str = 'http://source_processor:8080'

    capture_timeout: PositiveFloat = 1
    capture_max_retries: PositiveInt = 3
    capture_retries_interval: PositiveFloat = 0.1


class SearchEngineSettings(BaseModel):
    url: str = 'http://search_engine:8080'


class PostgresSettings(BaseModel):
    url: PostgresDsn = ('postgresql+asyncpg://'
                        'postgres:postgres@postgres:5432/postgres')

    @validator('url')
    def validate_url(cls, v: PostgresDsn):
        if v.scheme == 'postgresql+asyncpg':
            return v
        raise ValidationError('Only postgresql+asyncpg scheme is supported')


class RabbitMQSettings(BaseModel):
    video_chunks_exchange: str = 'video_chunks'


class PathsSettings(BaseModel):
    chunks_dir: Path = Path('./video_data/chunks')
    sources_dir: Path = Path('./video_data/sources')
    credentials: Path = Path('./credentials/credentials.json')


class VideoSettings(BaseModel):
    frame_width: int = Field(640, ge=28, le=1920)
    frame_height: int = Field(480, ge=28, le=1080)
    chunk_duration: float = Field(60, gt=1, le=600)
    chunk_fps: float = Field(1, gt=0, le=60)


class Settings(BaseSettings):
    api: ApiSettings = ApiSettings()
    source_processor: SourceProcessorSettings = SourceProcessorSettings()
    search_engine: SearchEngineSettings = SearchEngineSettings()
    postgres: PostgresSettings = PostgresSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    paths: PathsSettings = PathsSettings()
    video: VideoSettings = VideoSettings()

    class Config:
        env_nested_delimiter = '__'


settings = Settings()

settings.paths.chunks_dir.mkdir(parents=True, exist_ok=True)
settings.paths.sources_dir.mkdir(parents=True, exist_ok=True)
settings.paths.credentials.parent.mkdir(parents=True, exist_ok=True)

settings.paths.chunks_dir = settings.paths.chunks_dir.resolve()
settings.paths.sources_dir = settings.paths.sources_dir.resolve()
settings.paths.credentials = settings.paths.credentials.resolve()
