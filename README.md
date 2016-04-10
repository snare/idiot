# idiot

*Your best is an idiot.*

Idiot is an OS X tool for reminding you not to be stupid.

* Ever turn off your firewall because that Meterpreter callback wasn't working and then forget to turn it back on?
* Ever run Apache to test something and forget to kill it?
* Ever spin up a MongoDB instance in Docker and accidentally leave it running with no password and a ton of production data in it?

Idiot is the tool for you. Idiot runs checks (written in Python) every now and then, and if it finds something is awry it will throw up a notification dialog and put an indicative icon in the OS X status bar. It will keep reminding you every time it checks, until you either "snooze" notifications for that particular check or defenestrate your machine.

Built-in checks:

* Apache
* Firewall
* Docker
* Vagrant
* ARDAgent
* File sharing
* Screen sharing
* SSH

## Installation

Download the latest binary [here](https://github.com/snare/idiot/releases), unzip the zip file and drag the app to the `/Applications` folder.

## Building

To build the app:

    $ python setup.py py2app

## Running

Launch `Idiot.app`.

Alternatively, you can run Idiot from the command line. The only caveat is that you will get a Python icon in the dock.

    $ python setup.py install
    $ idiot

### Status Menu

Idiot adds an icon to the OS X status bar. Hopefully this will be a happy face telling you everything is OK. If something goes wrong, the icon changes. The menu underneath the icon reflects the status of the most recent run of checks:

![status_menu](http://i.imgur.com/ZwAAfna.png)

### Notifications

Whenever a check is failed, a notification is displayed via OS X's Notification Center. Notifications have 2 buttons: "Dismiss" and "Snooze". "Dismiss" simply closes the notification. "Snooze", however, notifies Idiot that you'd like to temporarily disable notifications for this particular check.

![notification](http://i.imgur.com/YzlteKX.png)

Snoozing uses a series of intervals (by default 1hr, 6hrs and forever) so the first time you snooze for a check it will disable notifications for the first interval (e.g. 1hr). If you hit snooze again it'll disable for the second interval (e.g. 6hrs), and if you hit snooze a third time it will disable for the 3rd interval (e.g. forever by default). "Forever" in this instance means "until the check is passed again" (so, until the firewall is enabled and Idiot checks it again, for example). Snooze state does not persist across restarts of Idiot.

## Configuration

Create a file at `~/.idiot/config` to customise configuration. See `config/default.conf` in the package for more info. You can probably guess.

## Extending

See `checks/*` in the `idiot` package for examples.

User-defined checks are placed in `~/.idiot/checks`.

New checks must be explicitly enabled in config. Edit your `~/.idiot/config` and copy in the list of enabled checks from `config/default.conf`, then add your user check's class name to the list:

    enabled:
      - ApacheCheck
      ...
      - MyUserCheck

When testing, you might want to edit your config to enable debug logging, make the checks run more frequently and lower the snooze intervals with a config like this:

    debug_logging:  true
    check_interval: 10
    snooze_intervals: [60, 120, 'forever']

## License

See LICENSE file.