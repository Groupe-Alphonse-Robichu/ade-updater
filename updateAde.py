#!/usr/bin/python3
import logging
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

from icalendar.discover import discoverAllGroups, discoverAll, discoverRemaining
from icalendar.update import updateAllGroups
from icalendar.creation import createCalendar, createCalendarGroup
from icalendar.notifiers.terminal import TerminalNotifier
from icalendar.notifiers.discord import DiscordNotifier
from sources import getSources

import sys


def help(exit_code=0) :
	script_name = sys.argv[0]
	print(f"usage : {script_name} --createGroup <group_name> <source_name>")
	print(f"        {script_name} --createCal <group_name> <cal_name>")
	print(f"        {script_name} --sources")
	print(f"        {script_name} [-n] --update")
	print(f"        {script_name} [-n] --all")
	print(f"        {script_name} [-n] --remaining")
	sys.exit(exit_code)


if __name__ == '__main__' :

	args = sys.argv[1:]

	if len(args) > 0 and args[0] == '-n' :
		args = args[1:]
		notifier = TerminalNotifier()
	else :
		notifier = DiscordNotifier()
	
	if len(args) > 0 and args[0] in ['-h', '--help'] :
		help(0)

	if len(args) == 0 :
		help(1)
	
	if args[0] == '--update' :
		updateAllGroups(notifier)
		sys.exit(0)
	
	if args[0] == '--all' :
		discoverAllGroups(discoverAll, notifier)
		sys.exit(0)
	
	if args[0] == '--remaining' :
		discoverAllGroups(discoverRemaining, notifier)
		sys.exit(0)
	
	if args[0] == '--sources' :
		for source in getSources() :
			print(source)
		sys.exit(0)

	if args[0] == '--createGroup' :
		if len(args) < 3 :
			help(1)
		sys.exit(0 if createCalendarGroup(args[1], args[2]) else 1)
		
	
	if args[0] == '--createCal' :
		if len(args) < 3 :
			help(1)
		sys.exit(0 if createCalendar(args[1], args[2]) else 1)

