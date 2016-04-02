"""
Vagrant check for Idiot.
"""
import logging
import subprocess

import idiot
from idiot import CheckPlugin

log = logging.getLogger()


class VagrantCheck(CheckPlugin):
    name = "Vagrant"

    def run(self):
        try:
            output = subprocess.check_output(["vagrant global-status"], shell=True).split('\n')[2:]
            running = [line.split()[0] for line in output if "running" in line]
            if len(running):
                return (False, "VMs are running: {}".format(', '.join(running)))
            else:
                return (True, "no VMs are running")
        except Exception as e:
            log.exception("Failed to get `vagrant global-status` output")
            return (False, "failed to get `vagrant global-status` output")


if __name__ == "__main__":
    print(VagrantCheck().run())
