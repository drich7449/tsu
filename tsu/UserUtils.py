from functools import lru_cache
from pwd import getpwnam
from pathlib import PurePath, Path


class UserUtils:
    console = "hit"

    @lru_cache(maxsize=4)
    def is_other_user(self, user_n, uid):
        console = self._conlog_.get_console()
        if user_n == 0 or user_n == "root" or (not user_n):
            return False
        target_uid = getpwnam(user_n).pw_uid
        is_other = (target_uid != 0) and (target_uid != uid)
        console.debug(r" {user_n=} {uid=} {target_uid=} {is_other=}")
        return is_other


def hist_file(shell):
    shellname = PurePath(shell).name
    histfile = Path.home() / f"{shellname}_history_root"
    return str(histfile)
