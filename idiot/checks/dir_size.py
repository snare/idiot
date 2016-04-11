"""
Idiot check if a directory is using more than X disk space

purpose: useful for when you use programs that spit out massive amounts of data
and you are blissfully unaware until your system disk is full (hello burpsuite auto-backup)

requirement: none

"""

import os

import idiot
from idiot import CheckPlugin


class DirSizeCheck(CheckPlugin):
    name = "directory size"

    def run(self):
        """
        Run the check.

        All check scripts must implement this method. It must return a tuple of:
        (<success>, <message>)

        In this example, if the check succeeds and FileSharing processes are nowhere
        to be found, the check will return (True, "all directories smaller than their configured limits").

        If the check fails and an FileSharing process is found, it returns
        (False, "[message including directories that are larger than their limits")
        """
        over_full_dirs = []
        if idiot.config.dir_size != None:
            for d in idiot.config.dir_size:
                size = self.get_size(d['path']) / float(1<<20) #convert from bytes to MB
                if size > d['limit']:
                    over_full_dirs.append(d['path'])
            if len(over_full_dirs) == 1:
                return (False, "found a directory larger than its configured limit: " + str(over_full_dirs[0]))
            if len(over_full_dirs) > 1:
                return (False, "found directories larger than their configured limits: {}".format(', '.join([str(d) for d in over_full_dirs])))
            return (True, "all directories smaller than their configured limits")
        else:
            return (True, "no directories specified")

    def get_size(self, start_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

if __name__ == "__main__":
    print(DirSizeCheck().run())
