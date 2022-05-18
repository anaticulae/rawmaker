# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import pytest
import serializeraw
import utila
import utilatest

import rawmaker
import tests

ARCHIVE = utila.join(rawmaker.ROOT, 'tests/images/expected', exist=True)


@pytest.mark.parametrize('source, pages', [
    pytest.param(power.MASTER105_PDF, '30:40', id='master105'),
])
def test_validate_images(source, pages, testdir, monkeypatch):
    Evaluate(
        source=source,
        pages=pages,
        expected=utila.file_name(source),
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, monkeypatch):
        super().__init__(
            step=f'images -i {source}',
            program=functools.partial(tests.run, monkeypatch=monkeypatch),
            pages=pages,
            source=source,
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.load_images,
            convert_source=False,
            index=expected,
        )

    def load_images(self, _):  # pylint:disable=W0613
        path = utila.join(self.workdir, 'rawmaker__images_images')
        images = serializeraw.load_image_infos_frompath(path)
        result = utila.flatten_content(images)
        return result

    def raw(self, value) -> str:
        return utila.NEWLINE.join(rawline(item) for item in value)


def rawline(image) -> str:
    page = str(image.page).zfill(3)
    bounding = utila.from_tuple(utila.roundme(image.bounding))
    line = f'{page} {bounding}'
    return line
