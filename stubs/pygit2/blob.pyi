import io
import types
from _typeshed import WriteableBuffer
from contextlib import AbstractContextManager

from ._pygit2 import Blob, Oid
from .enums import BlobFilter

class _BlobIO(io.RawIOBase):
    def __init__(
        self,
        blob: Blob,
        as_path: str | None = None,
        flags: BlobFilter = ...,
        commit_id: Oid | None = None,
    ) -> None: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None: ...
    def isatty() -> bool: ...  # type: ignore[misc]
    def readable(self) -> bool: ...
    def writable(self) -> bool: ...
    def seekable(self) -> bool: ...
    def readinto(self, b: WriteableBuffer, /) -> int: ...
    def close(self) -> None: ...

class BlobIO(io.BufferedReader, AbstractContextManager[_BlobIO]):  # type: ignore[misc]
    def __init__(
        self,
        blob: Blob,
        as_path: str | None = None,
        flags: BlobFilter = ...,
        commit_id: Oid | None = None,
    ) -> None: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None: ...
