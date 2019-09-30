# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

import os
from . import consts
from pathlib import Path, PurePath


def hist_file(shell):
    shellname = PurePath(shell).name
    histfile = Path.home() / f"{shellname}_history_root"
    return str(histfile)
