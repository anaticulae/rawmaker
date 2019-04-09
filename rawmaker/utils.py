#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from sys import platform


def fix_encoding(msg: str):
    """Remove invalid character to display on console

    Args:
        msg(str): message with invalid character
    Returns:
        message `without` invalid character"""

    # ensure to have str
    msg = str(msg)

    # Convert for windows console, replace non supported chars
    encoding = 'cp1252' if platform in ('win32', 'cygwin') else 'utf-8'

    # remove non valid char to avoid error on (win)-console
    msg = msg.encode(encoding, errors='xmlcharrefreplace').decode(encoding)
    return msg
