# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import rawmaker.features.annotation
import rawmaker.reader


def test_annotation_mining_annotations(capsys):
    extracted = None
    with rawmaker.reader.read(power.DOCU013_PDF) as pdf:
        extracted = rawmaker.features.annotation.extract_annotations(pdf)
    # 8 pages with annotation, skip empty one
    assert len(extracted) == 8
    # no logging errors from unsupported annotation
    assert not utilatest.stderr(capsys)


def test_annotation_work():
    result = rawmaker.features.annotation.work(power.DOCU013_PDF)
    assert len(result) > 200


@pytest.fixture
def vim_guide_annotation():
    extracted = None
    with rawmaker.reader.read(power.DOCU013_PDF) as pdf:
        extracted = rawmaker.features.annotation.extract_annotations(pdf)
    return extracted


def test_annotation_dump_and_load(vim_guide_annotation):  #pylint:disable=W0621
    annotation = vim_guide_annotation
    without_none = [
        item for item in annotation if item.pagelinks or item.hyperlinks
    ]
    dumped = serializeraw.dump_annotations(annotation)
    loaded = serializeraw.load_annotations(dumped)
    assert loaded == without_none


# TODO: Extend annotation parser to support book053
SKIP = {power.BOOK053_PDF}
TODO = [
    pytest.param(pdf, id=utila.file_name(pdf))
    for pdf in power.PDF
    if pdf not in SKIP
]


@pytest.mark.parametrize('source', TODO)
@utilatest.longrun
def test_annotation_x(source, capsys):
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.features.annotation.extract_annotations(pdf)
    for page in extracted:
        for hyperlink in page.hyperlinks or []:
            assert hyperlink.goal, str(hyperlink)
        for pagelink in page.pagelinks or []:
            assert pagelink.goal, str(pagelink)
    extracted = serializeraw.dump_annotations(extracted)
    assert 'PDFObjRef' not in extracted, 'improve annotation parser'
    assert 'python/object' not in extracted, 'improve annotation parser'
    error = utilatest.stderr(capsys)
    assert '[ERROR]' not in error, error
