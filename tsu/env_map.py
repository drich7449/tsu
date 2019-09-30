import os
from pathlib import Path

import attr

from conlog import Conlog
from .UserUtils import UserUtils
from . import consts


def init(_conlog, level, enabled):
    global conlog
    global user_utils
    conlog = _conlog
    user_utils = _conlog.fngrp(UserUtils, level, enabled)


class EnvMap:
    _ENV_CLEAN_BASE = {"ANDROID_DATA": "/data", "ANDROID_ROOT": "/system"}

    _ENV_CLEAN_BASE_COPY = ["EXTERNAL_STORAGE", "LANG", "TERM"]

    _ENV_CLEAN_OTHER = {"HOME": "/", "PATH": "/system/bin:/system/xbin"}

    def __init__(self, prepend=False, clean=False, usern="root"):
        self.prependpath = prepend
        self.cleanenv = clean
        self.usern = usern

    @property
    def shell(self):
        return self._shell

    @shell.setter
    def shell(self, shell):
        self._shell = shell

    @property
    def c_uid(self):
        return self._cuid

    @c_uid.setter
    def c_uid(self, c_uid):
        self._cuid = c_uid
        self.is_other_user = user_utils.is_other_user(self.usern, self._cuid)
        conlog.debug(r"current_uid {self.is_other_user=}")

    def getEnv(self):

        if self.is_other_user:
            pass
        if self.cleanenv:
            return self.clean_root
        pass

    def getShell(self):
        shell_name = GetShell(self._shell, self.is_other_user).get()
        conlog.debug(r"{shell_name=}")
        return shell_name

    @classmethod
    def __merge_base(E):
        env_b = E._ENV_CLEAN_BASE
        env_bcp = {key: os.environ[key] for key in E._ENV_CLEAN_BASE_COPY}
        return {**env_b, **env_bcp}

    @property
    def unclean_other(self):
        env_copy = os.environ
        env_copy["PATH"]

    def add_to_path(self, env_path, prep_path):
        front = self.prependpath
        sep = os.pathsep
        new_path = (
            f"{prep_path}{sep}{env_path}" if front else f"{env_path}{sep}{prep_path}"
        )
        return new_path

    @property
    def clean_other(self):
        E = EnvMap
        environ = E.__merge_base()
        return {**environ, **E._ENV_CLEAN_OTHER}

    @property
    def clean_root(self):
        E = EnvMap
        environ = E.__merge_base()
        PREFIX = consts.TERMUX_PREFIX
        PATH = self.add_to_path(
            f"{PREFIX}/bin:${PREFIX}/bin/applets", consts.ANDROIDSYSTEM_PATHS
        )
        env_root = {
            "HOME": "data/data/com.termux/files/home",
            "PATH": PATH,
            "PREFIX": f"{PREFIX}",
            "TMPDIR": f"{PREFIX}/tmp",
        }
        environ = {**environ, **env_root}
        return environ


@attr.s(auto_attribs=True)
class GetShell:
    shell: str
    is_termux_user: bool

    def get(self):
        root_shell = consts.SYS_SHELL
        USER_SHELL = Path(Path.home(), ".termux/shell")
        BASH_SHELL = Path(consts.TERMUX_PREFIX, "bin/bash")

        shell = self.shell
        # Others user cannot access Termux environment
        # The Android system shell.
        if shell == "system":
            root_shell = consts.SYS_SHELL
        # Check if user has set a login shell
        elif USER_SHELL.exists():
            root_shell = str(USER_SHELL.resolve())
        # Or at least installed bash
        elif BASH_SHELL.exists():
            root_shell = str(BASH_SHELL)
        return root_shell
