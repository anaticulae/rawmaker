# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

import pdfinfo
import serializeraw
import utila

import linero
import linero.table.camelox

RUNTIME = os.path.join(linero.ROOT, 'linero/camelox/runtime.py')
utila.exists_assert(RUNTIME)


def run(pdffile, pages: tuple = None, worker: int = 1):
    if not utila.exists(pdffile):
        return []
    pages = determine_pages(pdffile, pages)
    grouped = utila.xsome(pages, count=worker)
    todo = [functools.partial(single, pdffile, page) for page in grouped]
    todo = utila.fork(*todo, worker=worker)
    # prepare result
    dones = [done.stdout.strip() for done in todo]
    raw = '\n'.join(dones)
    result = serializeraw.load_tables(raw)
    return result


def single(pdffile, page):
    page = utila.from_tuple(page, separator='_')
    cmd = f'python {RUNTIME} {pdffile} {page}'
    cmd = utila.forward_slash(cmd, newline=False)
    completed = utila.run(cmd)
    return completed


def determine_pages(pdffile, pages: tuple = None):
    pagesmax = pdfinfo.pagecount(pdffile)
    if pages is None:
        return list(range(pagesmax))
    return [
        page for page in range(pagesmax) if not utila.should_skip(page, pages)
    ]
