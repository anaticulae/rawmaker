# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pdfminer.utils
import utila

import rawmaker.reader


def determine(path: str) -> dict:
    result = {}
    with rawmaker.reader.read(path) as document:
        infos = document.info
        if not infos:
            # no meta information available
            utila.error(f'could not read any meta information: {path}')
            return {}
        assert len(infos) == 1, str(infos)
        infos = infos[0]
        for key, value in infos.items():
            key = key.lower()
            if isinstance(value, bytes):
                # SEE PDFDocEncoding Character Set
                result[key] = pdfminer.utils.decode_text(value)
            else:
                result[key] = utila.str2bool(value.name)
    return result
