# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

import os
import sys

import os
import pwd
from pathlib import Path, PurePath

from docopt import docopt
from conlog import Conlog

from tsu import consts
from .su_bin import magisk, losu, chsu

import tsu.exec
from tsu.exec import VerCmp
import tsu.env_map
from tsu.env_map import EnvMap


def cli():
    """
    tsu A su interface wrapper for Termux

    Usage: 
        tsu
        tsu [ -s SHELL ]  [-pe] [USER] 
        tsu --debug [ -s SHELL ]  [-pel] [USER]
        tsu -h | --help | --version 
        

    Options:
    -s <shell>   Use an alternate specified shell.
    -l           Start a login shell.
    -p           Prepend system binaries to PATH
    -e           Start with a fresh environment.
    --debug      Output debugging information to stderr.
    -h --help    Show this screen.
    --version    Show version.

    """

    args = docopt(cli.__doc__)
    cur_uid = os.getuid()

    ### Debug handler
    debug_enabled = True if args["--debug"] else False
    conlog = Conlog("__main__", Conlog.DEBUG, enabled=debug_enabled)
    # conlog.dir(args)
    tsu.env_map.init(conlog, Conlog.DEBUG, enabled=debug_enabled)
    tsu.exec.init(conlog, Conlog.DEBUG, enabled=debug_enabled)
    ver_cmp = conlog.fngrp(VerCmp, Conlog.DEBUG, enabled=debug_enabled)
    ### Debug handler

    ### Setup Shell and Enviroment
    env_new = EnvMap(
        prepend=(args.get("-p")), clean=(args.get("-e")), usern=(args.get("USER"))
    )
    env_new.c_uid = cur_uid
    env_new.shell = args.get("-s")

    env = env_new.getEnv()
    shell = env_new.getShell()
    # Check `su` binaries:
    su_bins = [magisk, losu, chsu]
    for su_bin in su_bins:
        result = ver_cmp.compare(su_bin)

        if result:
            ver_cmp.call_su(su_bin, args.get("USER"), shell, env)
            break

    print("su binary not found.")
    print("Are you rooted? ")
