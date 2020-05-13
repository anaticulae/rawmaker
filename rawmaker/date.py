# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Date
====

See 7.9.4.

Format: (D:YYYYMMDDHHmmSSOHH'mm)
YYYY: Year
MM: Month(01-12)
DD: Day(0-31)
HH: Hour(0-23)
mm: minute(00-59)
SS: second(00-59)
O: + or -
HH: offset in hours
'
mm: offset in minutes
"""

import dataclasses
import re

PATTERN = (r'D:(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})'
           r'(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})(?P<sign>[+-])'
           r'(?P<utc_hour>\d{2})\'(?P<utc_minute>\d{2})')


@dataclasses.dataclass
class PDFDate:
    year: int = None
    month: int = None
    day: int = None
    hour: int = None
    minute: int = None
    second: int = None
    utc_hour: int = None
    utc_minute: int = None

    @property
    def raw(self) -> str:
        sign = '+' if self.utc_hour >= 0 else '-'
        result = (f'D:{self.year:04d}{self.month:02d}{self.day:02d}'
                  f'{self.hour:02d}{self.minute:02d}{self.second:02d}'
                  f'{sign}{self.utc_hour:02d}\'{self.utc_minute:02d}')
        return result


def parse(item: str) -> PDFDate:
    """Parse ASN.1 date pattern

    >>> parse("D:20160419072554+02'00")
    PDFDate(year=2016, month=4, day=19, hour=7, minute=25, second=54, utc_hour=2, utc_minute=0)
    """
    matched = re.match(PATTERN, item)
    if not matched:
        return None
    values = [
        'day', 'hour', 'minute', 'month', 'second', 'year', 'utc_hour',
        'utc_minute'
    ]
    data = {key: int(matched[key]) for key in values}
    result = PDFDate(**data)
    if matched['sign'] == '-':
        result.hour = result * -1
    return result
