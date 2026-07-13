"""Cross-platform exclusive file lock for critic sessions."""

from __future__ import annotations

import os
import sys
from types import TracebackType
from typing import IO


class FileLock:
    """Exclusive lock over an open file handle (POSIX fcntl or Windows msvcrt)."""

    def __init__(self, handle: IO[str]):
        self._handle = handle
        self._locked = False

    def acquire(self) -> None:
        if self._locked:
            return
        if sys.platform == "win32":
            import msvcrt

            self._handle.seek(0)
            # Lock one byte at start of file.
            msvcrt.locking(self._handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl

            fcntl.flock(self._handle.fileno(), fcntl.LOCK_EX)
        self._locked = True

    def release(self) -> None:
        if not self._locked:
            return
        if sys.platform == "win32":
            import msvcrt

            self._handle.seek(0)
            msvcrt.locking(self._handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(self._handle.fileno(), fcntl.LOCK_UN)
        self._locked = False

    def __enter__(self) -> FileLock:
        self.acquire()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.release()


def ensure_lock_file(path: os.PathLike[str] | str) -> None:
    path_str = os.fspath(path)
    if not os.path.exists(path_str):
        with open(path_str, "a", encoding="utf-8"):
            pass
