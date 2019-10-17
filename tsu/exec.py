# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

import subprocess
import re

from pathlib import Path
from . import consts

from conlog import Conlog


def init(_conlog, level, enabled):
    global conlog
    global user_utils
    conlog = _conlog


class VerCmp:
    def call_su(self, su, usern, shell, env=None):
        console = self._conlog_.get_console()

        su_path = su.lpath()
        argv = [su.argmap["shell"], shell]
        init = su.argmap.get("init", False)
        if init:
            argv = [init, *argv]
        if usern:
            argv = [*argv, usern]
        console.debug("Calling {su_path=} with {usern=} {argv=} and with enviroment")
        if env:
            console.dir(env)
        linux_execve(su_path, argv, env=env)
        return True

    def compare(self, su):
        console = self._conlog_.get_console()
        name = su.name
        su_path = su.lpath()
        checkver = [su_path] + su.veropt
        if su.multipath:
            print(consts.CHSU_WARN)
            return False
        try:
            ver = subprocess.check_output(checkver).decode("utf-8")
            console.debug(r" {name=} {ver=}")
            found = True if su.verstring in ver else -4
            return found
        except FileNotFoundError:
            return False
        except PermissionError:
            return False


def linux_execve(cmd, args, env=None):
    exec = [cmd] + args
    subprocess.run(exec, env=env)
