# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import io


def image_tobytes(image) -> bytes:
    raw = io.BytesIO()
    image.save(raw, format='PNG')
    raw.seek(0)
    result = raw.getvalue()
    return result
