"""
File watcher for Idiot.

This check takes an initial snapshot of the specified files, and then each time
the check is run it compares the current state of the files to the stored
snapshot. If the files differ, the check fails.

This check might be useful for situations where config options are changed
temporarily (change log level for SSH config, add a listener for Apache) and
then not changed back.

Files to watch are defined in Idiot's config.

To take a snapshot, run this check from the command line with the `--snapshot`
arg:

$ python idiot/checks/watch.py --snapshot
"""

import argh
import shutil
import uuid
import yaml
import logging
import difflib

import idiot
from idiot import CheckPlugin
from scruffy import Directory, File

log = logging.getLogger()


class FileWatcherCheck(CheckPlugin):
    name = "File watcher"

    def __init__(self, *args, **kwargs):
        super(FileWatcherCheck, self).__init__(*args, **kwargs)
        idiot.env.main_dir.add(watch_dir=Directory('watch_snapshot'))
        self.wd = idiot.env.main_dir.watch_dir

    def run(self):
        try:
            manifest = yaml.safe_load(self.wd.read('manifest'))
        except:
            log.error("No snapshot found")
            return (False, "no snapshot found")

        fails = []
        for filepath in manifest:
            f = File(filepath)
            s = File(manifest[filepath], parent=self.wd)
            diff = list(difflib.unified_diff(f.content.splitlines(), s.content.splitlines()))
            if len(diff):
                fails.append(filepath)
                log.info("Check for {} failed with diff:")
                log.info("\n".join(diff))

        if len(fails):
            return (False, "the following files have changed: {}".format(', '.join(fails)))
        else:
            return (True, "no files have changed")

    def snapshot(self):
        self.wd.remove()
        self.wd.create()
        manifest = {}

        for filepath in idiot.config.watch_files:
            f = File(filepath)
            try:
                newf = self.wd.add(File(uuid.uuid4().hex))
                newf.write(f.content)
                manifest[filepath] = newf.name
            except:
                log.exception("Exception copying file for snapshot")
        self.wd.write('manifest', yaml.dump(manifest))


@argh.arg('-s', '--snapshot', help='Take a new snapshot of the specified config files', default=False)
def run(snapshot=False):
    if snapshot:
        FileWatcherCheck().snapshot()
    else:
        print(FileWatcherCheck().run())


if __name__ == "__main__":
    argh.dispatch_command(run)
