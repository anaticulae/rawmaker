#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Table of content.

Basic structure of get_outlines: (level, title, args, children)
"""

from iamraw import Section
from iamraw import Toc
from yaml import dump
from yaml import FullLoader
from yaml import load

# TODO: Move Section to `IAmRaw`


def parse_toc(outlines):
    """Extract toc out of pdf-outlines

    The highest level is 0 the document root. Higher number level means more
    distance to root.
    """
    root = Toc()
    current = root
    for item in outlines:
        level = item.level
        if level == current.level:
            # Content is on the same level, therefore they have the same
            # parent together.
            new_one = Section(
                parent=current.parent,
                level=item.level,
                title=item.title,
            )
            add_children(current.parent, new_one)
        elif level > current.level:
            # The level of the item to add is higher than the current item in
            # table of content, therefore add the new one as a paranet of
            # current.
            new_one = Section(
                parent=current,
                level=item.level,
                title=item.title,
            )
            add_children(current, new_one)
        else:
            # The level of the `new_one` is lower than the item in index. That
            # means that the distance of the item to add to the index is
            # samller as the current one.
            # For example: Current = 1.4.4.2
            #              item    = 1.5
            # We have to go up in the tree to find a common parent of both
            # and add item.
            while level <= current.level:
                if current.parent:
                    current = current.parent
                    continue
            new_one = Section(
                parent=current,
                level=item.level,
                title=item.title,
            )
            add_children(current, new_one)
        current = new_one
    return root


def add_children(section: Section, item):
    assert section, item
    section.children.append(item)


def dump_yaml(content: Toc):
    raw = _dump(content)
    return dump(raw)


def load_yaml(content: str):
    loaded = load(content, Loader=FullLoader)
    return _load(loaded, parent=None)


def _dump(current: Section):
    """Convert to raw python to have more clear yaml output"""
    children = [_dump(item) for item in current.children]
    try:
        result = {'level': current.level, 'title': current.title}
    except AttributeError:
        # Toc ROOT node
        result = {'level': 0}

    if children:
        result['children'] = children
    return result


def _load(current: dict, parent: Section):
    """Load from raw python without complex objects"""
    try:
        result = Section(
            level=current['level'],
            title=current['title'],
            parent=parent,
        )
    except KeyError:
        result = Toc()

    try:
        result.children = [_load(item, result) for item in current['children']]
    except KeyError:
        # A leaf has no childre
        pass
    return result
