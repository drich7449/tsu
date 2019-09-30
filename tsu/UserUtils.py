from functools import lru_cache
from pwd import getpwnam


class UserUtils:
    console = "hit"

    @lru_cache(maxsize=4)
    def is_other_user(self, user_n, uid):
        console = self._conlog_.get_console()
        console.debug(r"{user_n=} {uid=}")
        if  user_n == 0 or user_n == "root" or (not user_n):
            return False
        target_uid = getpwnam(user_n).pw_uid
        console.debug(r"{target_uid=}")
        is_other = (target_uid == 0) or (target_uid == uid)
        return is_other
