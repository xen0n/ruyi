from typing import TypeAlias

__all__ = [
    "__commit_id__",
    "__version__",
    "__version_tuple__",
    "commit_id",
    "version",
    "version_tuple",
]

_VersionTuple: TypeAlias = tuple[int | str, ...]
_CommitId: TypeAlias = str | None
version: str
__version__: str
__version_tuple__: _VersionTuple
version_tuple: _VersionTuple
commit_id: _CommitId
__commit_id__: _CommitId
