from enum import Enum


class ArchiveTypes(Enum):
    LZMA = 'xz'
    GZIP = 'gz'
    BZIP2 = 'bz2'
