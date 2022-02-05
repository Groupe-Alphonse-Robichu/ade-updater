#!/usr/bin/python3
from icalendar.discover import discoverAll, discoverAllGroups
from icalendar.update import updateAllGroups
from icalendar.notifiers.terminal import TerminalNotifier

import logging

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

notifier = TerminalNotifier()


# discoverAllGroups(discoverAll, notifier)

updateAllGroups(notifier)

