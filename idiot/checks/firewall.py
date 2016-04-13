"""
Firewall check for Idiot.
"""
import biplist

import idiot
from idiot import CheckPlugin


class FirewallCheck(CheckPlugin):
    name = "Firewall"

    def run(self):
        try:
            d = biplist.readPlist('/Library/Preferences/com.apple.alf.plist')
            enabled = (d['globalstate'] >= 1)
        except:
            return (False, "failed to read firewall config plist")

        return (enabled, "{}".format("enabled" if enabled else "disabled"))


if __name__ == "__main__":
    print(FirewallCheck().run())
