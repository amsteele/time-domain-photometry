from __future__ import annotations
import re
from pathlib import Path

def extract_filenum(path: Path) -> int | None:
    """Extract a file number from names like 20170421.036_cal_al.fits or 20170421.036.fits."""
    nm = path.name
    m = nm.split('_') 
    #print('m: ',m,m[0],m[0][-3:])
    if not m:
        return None
    return int(m[0][-3:])

def in_any_range(n: int, ranges) -> bool:
    for a, b in ranges:
        if a <= n <= b:
            return True
    return False
