"""Pydantic schemas for the data server."""

from pydantic import BaseModel
from app.models import UserRole, SourceStatus


class UserBase(BaseModel):
    name: str
    max_sources: int
    role: UserRole


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "admin",
                "role": 1,
                "max_sources": -1
            }
        }


class Source(BaseModel):
    id: int
    name: str
    url: str
    status_code: SourceStatus
    status_msg: str | None = None
    user_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Parking lot",
                "url": "http://example.com/video.mjpg",
                "status_code": 0,
                "status_msg": None
            }
        }


class VideoChunkBase(BaseModel):
    source_id: int
    file_path: str
    start_time: float
    end_time: float


class VideoChunkCreate(VideoChunkBase):
    pass


class VideoChunk(VideoChunkBase):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "source_id": 1,
                "file_path": "/path/to/chunk.mp4",
                "start_time": 0.0,
                "end_time": 10.0
            }
        }