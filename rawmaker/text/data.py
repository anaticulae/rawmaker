# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses

import iamraw
import utilo


@dataclasses.dataclass
class WordBoxPage:

    content: iamraw.BoundingBoxes = dataclasses.field(default_factory=list)
    page: int = None

    def __getitem__(self, index):
        return self.content[index]  # pylint:disable=E1136

    def __len__(self):
        return len(self.content)  # pylint:disable=E1136


WordBoxPages = list[WordBoxPage]


@dataclasses.dataclass
class PageLines:

    lines: list = dataclasses.field(default_factory=list)

    def __getitem__(self, index):
        return self.lines[index]  # pylint:disable=E1136

    def __len__(self):
        return len(self.lines)  # pylint:disable=E1136

    def __str__(self):
        word = lambda x: ''.join([char.text for char in x])  # pylint:disable=C3001
        line = lambda x: ' '.join([word(item) for item in x])  # pylint:disable=C3001
        lines = utilo.NEWLINE.join(line(item) for item in self.lines)  # pylint:disable=E1133
        return f'PageLines: {len(self.lines)}\n{lines}'
