#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from os.path import join

from tests.resource import HELLO_WORLD
from utila.test import run
from utila.test import skip_not_virtual

from rawmaker import ROOT


@skip_not_virtual
def test_run_rawmaker():
    install_and_run = 'python setup.py install && rawmaker --help'

    completed = run(install_and_run, cwd=ROOT)
    assert completed.returncode == 0, completed.stdout + completed.stderr


@skip_not_virtual
def test_pipe_from_and_into(tmpdir):
    result = join(tmpdir, 'raw.yaml')

    # command = 'cat %s | rawmaker > %s' % (HELLO_WORLD, result)
    command = 'cat %s | rawmaker ' % (HELLO_WORLD)

    completed = run(command, cwd=ROOT)
    msg = 'cmd: %s\n%s' % (command, str(completed))
    assert 'NotImplemented' in completed.stderr
    # assert completed.returncode == 0, msg


@skip_not_virtual
def test_input_and_pipe_into(tmpdir):
    result = join(tmpdir, 'raw.yaml')

    command = 'rawmaker -i %s > %s' % (HELLO_WORLD, result)

    completed = run(command, cwd=ROOT)
    msg = 'cmd: %s\n%s' % (command, str(completed))
    assert completed.returncode == 0, msg
