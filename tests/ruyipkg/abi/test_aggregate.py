from typing import Mapping

from ruyi.ruyipkg.abi.aggregate import build_summary
from ruyi.ruyipkg.abi.model import (
    AttributeVendorBlob,
    ElfABIRecord,
    ElfType,
    GnuProperty,
    VersionNeed,
)


def _rec(
    paths: tuple[str, ...] = ("x",),
    sha256: str = "0",
    e_machine: int = 62,
    elf_class: int = 64,
    endianness: str = "little",
    elf_type: ElfType = ElfType.DYN,
    is_dynamic: bool = True,
    interpreter: str | None = None,
    soname: str | None = None,
    needed: tuple[str, ...] = (),
    version_needs: tuple[VersionNeed, ...] = (),
    version_defs: tuple[str, ...] = (),
    gnu_properties: tuple[GnuProperty, ...] = (),
    elf_attributes: tuple[AttributeVendorBlob, ...] = (),
    parsed_attrs: Mapping[str, str | int | bool] | None = None,
    **kw: object,
) -> ElfABIRecord:
    return ElfABIRecord(
        paths=paths,
        sha256=sha256,
        e_machine=e_machine,
        elf_class=elf_class,
        endianness=endianness,
        elf_type=elf_type,
        is_dynamic=is_dynamic,
        interpreter=interpreter,
        soname=soname,
        needed=needed,
        version_needs=version_needs,
        version_defs=version_defs,
        gnu_properties=gnu_properties,
        elf_attributes=elf_attributes,
        parsed_attrs=parsed_attrs or {},
        **kw,
    )


def test_needed_union_sorted() -> None:
    recs = [_rec(needed=("libm.so.6",)), _rec(needed=("libc.so.6", "libm.so.6"))]
    summary = build_summary(recs, file_count=2, excluded_count=0)
    assert summary.needed == ("libc.so.6", "libm.so.6")


def test_well_known_maxima_picks_highest_glibc() -> None:
    recs = [
        _rec(version_needs=(VersionNeed("libc.so.6", ("GLIBC_2.17", "GLIBC_2.34")),)),
        _rec(version_needs=(VersionNeed("libc.so.6", ("GLIBC_2.9", "GLIBC_2.28")),)),
    ]
    summary = build_summary(recs, file_count=2, excluded_count=0)
    assert summary.well_known_maxima["GLIBC"] == "2.34"


def test_weak_versions_kept_separate_and_shadowed_by_strong() -> None:
    recs = [
        _rec(
            version_needs=(
                VersionNeed("libc.so.6", ("GLIBC_2.17",), ("GLIBC_2.9", "ZLIB_1.2")),
            )
        ),
        _rec(version_needs=(VersionNeed("libc.so.6", ("GLIBC_2.9",)),)),
    ]
    summary = build_summary(recs, file_count=2, excluded_count=0)
    assert summary.version_needs == (
        VersionNeed(
            "libc.so.6",
            ("GLIBC_2.17", "GLIBC_2.9"),
            ("ZLIB_1.2",),
        ),
    )


def test_rollup_x86_minimum_level() -> None:
    recs = [
        _rec(e_machine=62, parsed_attrs={"isa_level": "v3"}),
        _rec(e_machine=62, parsed_attrs={"isa_level": "v2"}),
    ]
    summary = build_summary(recs, file_count=2, excluded_count=0)
    assert summary.parsed_attrs_rollup["62"] == {
        "isa_level": "v2",
        "isa_levels": ["v2", "v3"],
    }


def test_counts_passthrough() -> None:
    summary = build_summary([_rec()], file_count=5, excluded_count=3)
    assert summary.elf_count == 1
    assert summary.file_count == 5
    assert summary.excluded_count == 3
    assert summary.e_machines == (62,)
