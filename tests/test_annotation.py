# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest

import rawmaker.features.annotation
import rawmaker.reader


def test_annotation_mining_annotations(capsys):
    extracted = None
    with rawmaker.reader.read(power.DOCU13_PDF) as pdf:
        extracted = rawmaker.features.annotation.extract_annotations(pdf)
    # 8 pages with annotation, skip empty one
    assert len(extracted) == 8
    # no logging errors from unsupported annotation
    assert not utilatest.stderr(capsys)


def test_annotation_work():
    result = rawmaker.features.annotation.work(power.DOCU13_PDF)
    assert len(result) > 200


@pytest.fixture
def vim_guide_annotation():
    extracted = None
    with rawmaker.reader.read(power.DOCU13_PDF) as pdf:
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


@pytest.mark.parametrize('source', [
    pytest.param(power.BACHELOR076_PDF, id='bachelor076'),
    pytest.param(power.MASTER075_PDF, id='master075'),
    pytest.param(power.MASTER155_PDF, id='master155'),
    pytest.param(power.DOCU013_PDF, id='docu013'),
    pytest.param(power.BACHELOR085_PDF, id='bachelor85'),
])
def test_annotation_x(source, capsys):
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.features.annotation.extract_annotations(pdf)
    for page in extracted:
        for hyperlink in page.hyperlinks or []:
            assert hyperlink.goal, str(hyperlink)
        for pagelink in page.pagelinks or []:
            assert pagelink.goal, str(pagelink)
    extracted: str = str(extracted)
    assert 'PDFObjRef' not in extracted, 'improve annotation parser'
    error = utilatest.stderr(capsys)
    assert '[ERROR]' not in error, error
