"""
Checks to ensure redis is not running
"""

import idiot
from idiot import ProcessCheck


class RedisCheck(ProcessCheck):
    name = "Redis"
    process_names = ["redis-server"]


if __name__ == "__main__":
    print(RedisCheck().run())
