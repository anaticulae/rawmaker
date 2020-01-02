# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# A3 = (297, 420)
# A4 = (210, 297)
# A5 = (148, 210)
# A6 = (104, 148)

MILI_TO_PIX = 0.35278413424866517, 0.3527514613989115


def tomilimeter(width: float, height: float):
    return round(width * MILI_TO_PIX[0]), round(height * MILI_TO_PIX[1])


def topixel(width: float, height: float) -> float:
    return (round(1.0 / MILI_TO_PIX[0] * width),
            round(1.0 / MILI_TO_PIX[1] * height))
