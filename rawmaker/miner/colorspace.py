# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib


def parse(image) -> str:
    colorspace = image.colorspace[0]
    if not colorspace:
        # TODO: VERIFY THIS
        return 'DeviceGray'
    colorspace = name(colorspace)
    # TODO: VERIFY R212!
    if colorspace in ('DeviceRGB', 'RGB', 'R213'):
        # RGB is an abbreviation of DeviceRGB
        return 'DeviceRGB'
    if colorspace in ('DeviceGray', 'G'):
        # G is an abbreviation of DeviceGray
        return 'DeviceGray'
    typ = colorspace[0].name
    if typ == 'Indexed':
        return indexed_space(*colorspace[1:])
    if typ == 'ICCBased':
        return iccbased(colorspace[1].resolve())
    return 'DeviceRGB'


def indexed_space(base, hival, lookup):  # pylint:disable=W0613
    base = name(base)
    # lookup = lookup.resolve()
    if base[0] == 'ICCBased':
        return iccbased(base[1].resolve())
    return None


def iccbased(stream) -> str:
    attributes = stream.attrs
    rawdata = stream.rawdata  # pylint:disable=W0612
    with contextlib.suppress(KeyError):
        colorspace = attributes['N']
        if colorspace == 1:
            colorspace = 'DeviceGray'
        elif colorspace == 3:
            colorspace = 'DeviceRGB'
        elif colorspace == 4:
            colorspace = 'DeviceCMYK'
    with contextlib.suppress(KeyError):
        colorspace = attributes['Alternate'].name
    return colorspace


def name(reference) -> str:
    with contextlib.suppress(AttributeError):
        reference = reference.resolve()
    with contextlib.suppress(AttributeError):
        return reference.name
    return reference
