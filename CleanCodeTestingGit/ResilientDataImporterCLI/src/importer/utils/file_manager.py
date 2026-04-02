from typing import IO


class FileManager:
    """
    Context manager for safe file handling.
    """

    def __init__(self, file_path: str, mode: str) -> None:
        self.file_path = file_path
        self.mode = mode
        self.file: IO | None = None

    def __enter__(self) -> IO:
        self.file = open(self.file_path, self.mode, encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.file:
            self.file.close()