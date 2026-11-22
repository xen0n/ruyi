import enum
import re
from typing import Final

from ..i18n import _

RE_TARBALL: Final = re.compile(r"\.tar(?:\.gz|\.bz2|\.lz4|\.xz|\.zst)?$")


class UnpackMethod(enum.StrEnum):
    UNKNOWN = ""
    AUTO = "auto"
    TAR_AUTO = "tar.auto"

    RAW = "raw"
    GZ = "gz"
    BZ2 = "bz2"
    LZ4 = "lz4"
    XZ = "xz"
    ZST = "zst"

    TAR = "tar"
    TAR_GZ = "tar.gz"
    TAR_BZ2 = "tar.bz2"
    TAR_LZ4 = "tar.lz4"
    TAR_XZ = "tar.xz"
    TAR_ZST = "tar.zst"

    ZIP = "zip"
    DEB = "deb"

    @property
    def is_tar(self) -> bool:
        return self.startswith("tar")

    @property
    def underlying_stream_format(self) -> "UnpackMethod":
        S = type(self)
        match self:
            case S.RAW | S.TAR | S.TAR_AUTO:
                return S.RAW
            case S.GZ | S.TAR_GZ:
                return S.GZ
            case S.BZ2 | S.TAR_BZ2:
                return S.BZ2
            case S.LZ4 | S.TAR_LZ4:
                return S.LZ4
            case S.XZ | S.TAR_XZ:
                return S.XZ
            case S.ZST | S.TAR_ZST:
                return S.ZST
            case _:
                # either truly unknown, or not single-stream
                return S.UNKNOWN


class UnrecognizedPackFormatError(Exception):
    def __init__(
        self,
        *,
        filename: str | None = None,
        fmt: UnpackMethod | None = None,
    ) -> None:
        if filename is None and fmt is None:
            raise ValueError("either filename or format must be provided")
        self.filename = filename
        self.fmt = fmt

    def __str__(self) -> str:
        if self.filename is not None:
            if self.fmt is not None:
                return _(
                    "don't know how to unpack file '{filename}' using format '{fmt}'"
                ).format(
                    filename=self.filename,
                    fmt=self.fmt,
                )
            return _("don't know how to unpack file '{filename}'").format(
                filename=self.filename,
            )
        return _("don't know how to unpack format '{fmt}'").format(
            fmt=self.fmt,
        )


def determine_unpack_method(
    filename: str,
) -> UnpackMethod:
    filename_lower = filename.lower()
    if m := RE_TARBALL.search(filename_lower):
        return UnpackMethod(m.group(0)[1:])
    if filename_lower.endswith(".deb"):
        return UnpackMethod.DEB
    if filename_lower.endswith(".zip"):
        return UnpackMethod.ZIP
    if filename_lower.endswith(".gz"):
        # bare gzip file
        return UnpackMethod.GZ
    if filename_lower.endswith(".bz2"):
        # bare bzip2 file
        return UnpackMethod.BZ2
    if filename_lower.endswith(".lz4"):
        # bare lz4 file
        return UnpackMethod.LZ4
    if filename_lower.endswith(".xz"):
        # bare xz file
        return UnpackMethod.XZ
    if filename_lower.endswith(".zst"):
        # bare zstd file
        return UnpackMethod.ZST
    return UnpackMethod.UNKNOWN
