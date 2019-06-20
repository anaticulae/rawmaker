# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import fixture

from rawmaker import read
from rawmaker.features.annotation import dump_annotations
from rawmaker.features.annotation import extract_annotations
from rawmaker.features.annotation import load_annotations
from tests.resource import VIM_GUIDE_PAGE_COUNT
from tests.resource import VIM_GUIDE_PDF


def test_annotation_mining_annotations(capsys):
    extracted = None
    with read(VIM_GUIDE_PDF) as pdf:
        extracted = extract_annotations(pdf)
    assert len(extracted) == VIM_GUIDE_PAGE_COUNT

    # no logging erros from unsupported annotation
    out, err = capsys.readouterr()
    assert not out
    assert not err


@fixture
def vim_guide_annotation():
    extracted = None
    with read(VIM_GUIDE_PDF) as pdf:
        extracted = extract_annotations(pdf)
    return extracted


def test_annotation_dump_and_load(vim_guide_annotation):  #pylint:disable=W0621
    annotation = vim_guide_annotation

    dumped = dump_annotations(annotation)

    loaded = load_annotations(dumped)

    # TODO: investigate here, why str matches and without str it does not
    # match?
    assert str(loaded) == str(annotation)
