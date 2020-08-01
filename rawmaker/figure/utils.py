# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import io

import PIL.Image
import utila


def image_tobytes(image) -> bytes:
    raw = io.BytesIO()
    image.save(raw, format='PNG')
    raw.seek(0)
    result = raw.getvalue()
    return result


WHITE = 1
RGBA = 'RGBA'


def rawfigure_frombounding(bbox, mode=RGBA, background=WHITE) -> PIL.Image:
    width = (bbox[2] - bbox[0])
    height = (bbox[3] - bbox[1])

    # ensure positive figure size
    if width < 0 or height < 0:
        utila.error(f'negative figure size: {width} {height}')
    width = utila.maxs(width, 1)
    height = utila.maxs(height, 1)

    size = (int(width), int(height))
    raw = PIL.Image.new(mode, size, color=background)
    return raw
