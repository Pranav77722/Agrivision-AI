import os
import uuid
import aiofiles
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class StorageService(ABC):
    @abstractmethod
    async def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str = "image/jpeg",
        folder: str = "uploads"
    ) -> str:
        """Upload file and return its accessible URL or path."""
        pass

    @abstractmethod
    async def get_file_path(self, relative_or_url: str) -> Optional[Path]:
        """Return local path to file if stored locally."""
        pass


class LocalStorageService(StorageService):
    def __init__(self, base_dir: str = settings.STORAGE_LOCAL_DIR):
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str = "image/jpeg",
        folder: str = "uploads"
    ) -> str:
        folder_dir = self.base_dir / folder
        folder_dir.mkdir(parents=True, exist_ok=True)

        ext = Path(filename).suffix or ".jpg"
        unique_name = f"{uuid.uuid4().hex}{ext}"
        target_path = folder_dir / unique_name

        async with aiofiles.open(target_path, "wb") as f:
            await f.write(file_bytes)

        logger.info(f"Saved file locally to {target_path}")
        # Public URL format served by FastAPI static mounting
        return f"/uploads/{folder}/{unique_name}"

    async def get_file_path(self, relative_or_url: str) -> Optional[Path]:
        # Handle '/uploads/...' or raw relative path
        clean_path = relative_or_url.lstrip("/")
        if clean_path.startswith("uploads/"):
            clean_path = clean_path[len("uploads/"):]
        target = self.base_dir / clean_path
        if target.exists():
            return target
        return None


class SupabaseStorageService(StorageService):
    """Supabase cloud storage provider with fallback to local storage."""

    def __init__(self):
        self.local_storage = LocalStorageService()
        self.supabase_url = settings.SUPABASE_URL
        self.service_key = settings.SUPABASE_SERVICE_KEY
        self.bucket = settings.SUPABASE_STORAGE_BUCKET

    async def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str = "image/jpeg",
        folder: str = "uploads"
    ) -> str:
        if not self.supabase_url or not self.service_key:
            # Fall back to local storage
            return await self.local_storage.upload_file(file_bytes, filename, content_type, folder)

        try:
            import httpx
            ext = Path(filename).suffix or ".jpg"
            remote_name = f"{folder}/{uuid.uuid4().hex}{ext}"
            upload_url = f"{self.supabase_url.rstrip('/')}/storage/v1/object/{self.bucket}/{remote_name}"

            headers = {
                "Authorization": f"Bearer {self.service_key}",
                "Content-Type": content_type,
            }
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(upload_url, headers=headers, content=file_bytes)
                if res.status_code in [200, 201]:
                    public_url = f"{self.supabase_url.rstrip('/')}/storage/v1/object/public/{self.bucket}/{remote_name}"
                    return public_url
                else:
                    logger.warning(f"Supabase upload returned {res.status_code}: {res.text}. Falling back to local.")
                    return await self.local_storage.upload_file(file_bytes, filename, content_type, folder)
        except Exception as e:
            logger.error(f"Supabase storage exception: {e}. Falling back to local.")
            return await self.local_storage.upload_file(file_bytes, filename, content_type, folder)

    async def get_file_path(self, relative_or_url: str) -> Optional[Path]:
        return await self.local_storage.get_file_path(relative_or_url)


class CloudinaryStorageService(StorageService):
    """Production Cloudinary storage service for uploaded crop leaf photos & heatmaps."""

    def __init__(self):
        self.local_storage = LocalStorageService()
        self.cloud_name = settings.CLOUDINARY_CLOUD_NAME
        self.api_key = settings.CLOUDINARY_API_KEY
        self.api_secret = settings.CLOUDINARY_API_SECRET
        self.base_folder = settings.CLOUDINARY_FOLDER or "Agrivision"

    async def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str = "image/jpeg",
        folder: str = "diagnoses"
    ) -> str:
        if not self.cloud_name or not self.api_key or not self.api_secret:
            logger.warning("Cloudinary credentials incomplete. Falling back to local storage.")
            return await self.local_storage.upload_file(file_bytes, filename, content_type, folder)

        try:
            import httpx
            import time
            import hashlib

            target_folder = f"{self.base_folder}/{folder}".strip("/")
            timestamp = int(time.time())

            # Cloudinary signing: parameters must be in alphabetical order
            params_to_sign = f"folder={target_folder}&timestamp={timestamp}{self.api_secret}"
            signature = hashlib.sha1(params_to_sign.encode("utf-8")).hexdigest()

            upload_url = f"https://api.cloudinary.com/v1_1/{self.cloud_name}/image/upload"

            files = {
                "file": (filename or "leaf.jpg", file_bytes, content_type)
            }
            data = {
                "api_key": self.api_key,
                "timestamp": str(timestamp),
                "folder": target_folder,
                "signature": signature,
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(upload_url, data=data, files=files)
                if res.status_code in [200, 201]:
                    json_res = res.json()
                    secure_url = json_res.get("secure_url") or json_res.get("url")
                    logger.info(f"Cloudinary upload successful to {target_folder}: {secure_url}")
                    return secure_url
                else:
                    logger.warning(f"Cloudinary upload failed ({res.status_code}): {res.text}. Falling back to local.")
                    return await self.local_storage.upload_file(file_bytes, filename, content_type, folder)
        except Exception as e:
            logger.error(f"Cloudinary upload exception: {e}. Falling back to local storage.")
            return await self.local_storage.upload_file(file_bytes, filename, content_type, folder)

    async def get_file_path(self, relative_or_url: str) -> Optional[Path]:
        return await self.local_storage.get_file_path(relative_or_url)


def get_storage_service() -> StorageService:
    if settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY and settings.CLOUDINARY_API_SECRET:
        return CloudinaryStorageService()
    if settings.SUPABASE_URL and settings.SUPABASE_SERVICE_KEY:
        return SupabaseStorageService()
    return LocalStorageService()
