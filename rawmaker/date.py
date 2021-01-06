# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Date
====

See Adobe PDF 2008 REF 7.9.4.

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

Parse and generate raw data again.

>>> time = "D:20160419072554+02'00"
>>> parsed = parse(time)

Convert parsed back to raw string

>>> raw(parsed)
"D:20160419072554+02'00"
"""

import dataclasses
import re


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


PATTERN = (r'D:(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})'
           r'(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})(?P<sign>[+-])'
           r'(?P<utc_hour>\d{2})\'(?P<utc_minute>\d{2})')


def raw(date: PDFDate) -> str:
    sign = '+' if date.utc_hour >= 0 else '-'
    result = (f'D:{date.year:04d}{date.month:02d}{date.day:02d}'
              f'{date.hour:02d}{date.minute:02d}{date.second:02d}'
              f'{sign}{date.utc_hour:02d}\'{date.utc_minute:02d}')
    return result


def parse(item: str) -> PDFDate:
    """Parse ASN.1 date pattern.

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
