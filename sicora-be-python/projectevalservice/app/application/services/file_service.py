import os
import aiofiles
from typing import Optional, List
from uuid import uuid4
import magic
from pathlib import Path

from ...config import settings


class FileService:
    """Service for handling file uploads and management"""

    def __init__(self):
        self.upload_path = Path(settings.upload_path)
        self.max_file_size = settings.max_file_size
        self.allowed_extensions = settings.allowed_file_extensions

        # Create upload directory if it doesn't exist
        self.upload_path.mkdir(parents=True, exist_ok=True)

    async def save_file(
        self, file_content: bytes, original_filename: str, project_id: str
    ) -> tuple[str, str, int]:
        """
        Save file to filesystem
        Returns: (file_path, file_name, file_size)
        """

        # Validate file size
        if len(file_content) > self.max_file_size:
            raise ValueError(
                f"File size exceeds maximum allowed size of {self.max_file_size} bytes"
            )

        # Validate file extension
        file_extension = Path(original_filename).suffix.lower()
        if file_extension not in self.allowed_extensions:
            raise ValueError(f"File extension {file_extension} is not allowed")

        # Generate unique filename
        unique_filename = f"{uuid4()}{file_extension}"

        # Create project-specific directory
        project_dir = self.upload_path / project_id
        project_dir.mkdir(exist_ok=True)

        # Full file path
        file_path = project_dir / unique_filename

        # Save file
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(file_content)

        return str(file_path), unique_filename, len(file_content)

    async def delete_file(self, file_path: str) -> bool:
        """Delete file from filesystem"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False

    async def get_file_content(self, file_path: str) -> Optional[bytes]:
        """Get file content"""
        try:
            async with aiofiles.open(file_path, "rb") as f:
                return await f.read()
        except Exception:
            return None

    def get_file_type(self, file_path: str) -> str:
        """Get MIME type of file"""
        try:
            return magic.from_file(file_path, mime=True)
        except Exception:
            return "application/octet-stream"

    def validate_file_type(self, file_content: bytes) -> bool:
        """Validate file type based on content"""
        try:
            mime_type = magic.from_buffer(file_content, mime=True)
            # Add specific MIME type validations if needed
            return True
        except Exception:
            return False

    def get_project_files(self, project_id: str) -> List[dict]:
        """Get all files for a project"""
        project_dir = self.upload_path / project_id
        if not project_dir.exists():
            return []

        files = []
        for file_path in project_dir.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                files.append(
                    {
                        "name": file_path.name,
                        "path": str(file_path),
                        "size": stat.st_size,
                        "created": stat.st_ctime,
                        "modified": stat.st_mtime,
                    }
                )

        return files
