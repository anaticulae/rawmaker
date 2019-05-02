#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import sys
from contextlib import suppress
from functools import partial

from pytest import raises

from rawmaker import PROCESS_NAME
from rawmaker.command import main

# from utila import run_command


# TODO: Remove after utila update
def run_command(command, monkeypatch, process, main, success=True):
    """Run `main` with `command`

    Args:
        command([str] or str): command to run
        monkeypatch: pytest patch feature
        process(str): name of executed tool
        main(callable): method to run
        success(bool): expectation that process succed or failes
    """
    with suppress(AttributeError):
        command = command.split()
    assert callable(main), str(main)

    with monkeypatch.context() as context:
        # proccess is removed as first arg
        context.setattr(sys, 'argv', [process] + command)
        with raises(SystemExit) as result:
            main()
        result = str(result)

    assert ('SystemExit: 0' in result) == success


#pylint: disable=invalid-name
run_success = partial(
    run_command,
    main=main,
    process=PROCESS_NAME,
    success=True,
)

run_failure = partial(
    run_command,
    main=main,
    process=PROCESS_NAME,
    success=False,
)
