# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import itertools

import iamraw
import serializeraw
import utila
import yaml

import rawmaker.math
import rawmaker.reader


def work(path: str, pages: tuple = None) -> str:
    with rawmaker.reader.read(path) as pdf:
        formulas = rawmaker.math.extract_content(pdf, pages=pages)
    dumped = serializeraw.dump_rawformulas(formulas)
    return dumped


def dump_rawformulas(pages: iamraw.PageContentRawFormulas) -> str:
    # remove empty pages
    result = [item.content for item in pages if item.content]
    result = utila.flatten(result)

    raw = [dump_formula(item) for item in result]

    # convert
    dumped = yaml.dump(raw)
    return dumped


def load_rawformulas(
        content: str,
        pages: tuple = None,
) -> iamraw.PageContentRawFormulas:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)

    loaded = [load_formula(item) for item in loaded]

    selected = [
        item for item in loaded if not utila.should_skip(item.page, pages)
    ]

    result = [
        iamraw.PageContentRawFormula(page=page, content=list(content))
        for page, content in itertools.groupby(selected, key=lambda x: x.page)
    ]

    return result


def dump_formula(formula: iamraw.FormulaRaw) -> dict:
    text = ''.join(item.value for item in formula.content)
    boundings = [utila.from_tuple(item.bounding) for item in formula.content]
    sizes = utila.from_tuple([item.size for item in formula.content])
    raw = {
        'text': text,
        'boundings': boundings,
        'sizes': sizes,
        'page': formula.page,
    }
    return raw


def load_formula(formula: dict) -> iamraw.FormulaRaw:
    text = formula['text']
    length = len(text)
    sizes = utila.parse_tuple(formula['sizes'], length=length)
    boundings = [utila.parse_tuple(item) for item in formula['boundings']]
    page = int(formula['page'])

    content = []
    for char, size, bounding in zip(text, sizes, boundings):
        content.append(
            iamraw.MathChar(
                value=char,
                bounding=bounding,
                size=size,
            ))
    result = iamraw.FormulaRaw(page=page, content=content)
    return result


serializeraw.dump_rawformulas = dump_rawformulas
serializeraw.load_rawformulas = load_rawformulas
