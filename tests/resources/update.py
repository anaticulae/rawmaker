# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import utila

import rawmaker
import tests.resources


def install_requirements():
    utila.clean_install(rawmaker.ROOT, 'rawmaker')


def sync_resources():
    completed = utila.run('power --all', tests.resources.RESOURCES)  # pylint:disable=C0103
    assert completed.returncode == utila.SUCCESS, str(completed)


def extract_examples():
    destination = tests.resources.GENERATED
    if os.path.exists(destination):
        return
    os.makedirs(destination)
    todo = [
        (tests.resources.LEFTRIGHT, tests.resources.LEFTRIGHT_GENERATED),
        (tests.resources.VIM_PDF, tests.resources.VIM_GENERATED),
    ]
    todo = [f'rawmaker -i {source} -o {dest} -j=8' for source, dest in todo]
    completed = utila.run_parallel(todo)
    assert completed == utila.SUCCESS


def install_and_run(root, package, executable=None):
    """Install and run --help to ensure basic function"""
    executable = executable if executable else package
    if isinstance(executable, str):
        executable = executable.split()
    uninstall = 'pip uninstall %s -y' % package

    executable = ' && '.join(['%s --help' % item for item in executable])
    install = 'python setup.py install && %s ' % executable

    clean_and_run = uninstall + ' && ' + install
    result = utila.run(clean_and_run, cwd=root)
    assert result.returncode == utila.SUCCESS, result.stdout + result.stderr
