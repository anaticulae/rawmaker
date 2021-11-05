# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import serializeraw
import utila

import rawmaker.cleanup.translate.lines


def work(
    text: str,
    text_baml: str,
    oneline_text: str,
    oneline_text_baml: str,
    pages: tuple = None,
) -> typing.Tuple[str, str]:
    text = determine_translation(
        source=text_baml,
        destination=text,
        pages=pages,
    )
    text_oneline = determine_translation(
        source=oneline_text_baml,
        destination=oneline_text,
        pages=pages,
    )
    result = (
        text,
        text_oneline,
    )
    return result


def determine_translation(source, destination, pages: tuple = None) -> str:
    if not utila.exists(source):
        return utila.NO_RESULT
    if not utila.exists(destination):
        return utila.NO_RESULT
    text_before = serializeraw.load_document(source, pages=pages)
    text = serializeraw.load_document(destination, pages=pages)
    text_translated = rawmaker.cleanup.translate.lines.translates(
        sources=text_before,
        destinations=text,
    )
    dumped = serializeraw.dump_translations(text_translated)
    return dumped
