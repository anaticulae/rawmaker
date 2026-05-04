# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import rawmaker
import tests

ARCHIVE = utilo.join(rawmaker.ROOT, 'tests/images/expected', exist=True)


@tests.ghost
@pytest.mark.parametrize('source, pages', [
    pytest.param(hoverpower.MASTER105_PDF, '30:40', id='master105'),
])
def test_validate_images(source, pages, td, mp):
    Evaluate(
        source=source,
        pages=pages,
        expected=utilo.file_name(source),
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilotest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, mp):
        super().__init__(
            step=f'images -i {source}',
            program=functools.partial(tests.run, mp=mp),
            pages=pages,
            source=source,
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.load_images,
            convert_source=False,
            index=expected,
        )

    def load_images(self, _):  # pylint:disable=W0613
        path = utilo.join(self.workdir, 'rawmaker__images_images')
        images = serializeraw.load_image_infos_frompath(path)
        result = utilo.flatten_content(images)
        return result

    def raw(self, value) -> str:
        return utilo.NEWLINE.join(rawline(item) for item in value)


def rawline(image) -> str:
    page = str(image.page).zfill(3)
    bounding = utilo.from_tuple(utilo.roundme(image.bounding))
    line = f'{page} {bounding}'
    return line
