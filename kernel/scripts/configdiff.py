#!/usr/bin/python
###############################################################################
# IPFire.org    - An Open Source Firewall Solution                            #
# Copyright (C) - IPFire Development Team <info@ipfire.org>                   #
###############################################################################

import re
import sys

filelist = sys.argv[1:]

options = []

f = open(filelist[0])
for line in f.readlines():
	# Strip newline.
	line = line.rstrip()

	option = value = None

	m = re.match("^# (.*) is not set$", line)
	if m:
		option = m.group(1)
		value  = "n"

	m = re.match("^(.*)=(.*)$", line)
	if m:
		option = m.group(1)
		value  = m.group(2)

	if option:
		option_value = "%s=%s" % (option, value or "")
		options.append(option_value)

f.close()

f = open(filelist[1])

section = None
for line in f.readlines():
	m = re.match("^# (.*)$", line)
	if m:
		_section = m.group(1)
		if not _section.startswith("CONFIG_") and \
				not _section.endswith("Kernel Configuration") and \
				not _section.startswith("Automatically generated file;"):
			section = _section
	elif not line:
		section = None

	option = None
	value  = None

	m = re.match("^# (.*) is not set$", line)
	if m:
		option = m.group(1)
		value  = "n"

	m = re.match("^(.*)=(.*)$", line)
	if m:
		option = m.group(1)
		value  = m.group(2)

	if not option:
		continue

	# Ignore all options CONFIG_HAVE_ because we cannot
	# set them anyway.
	elif option.startswith("CONFIG_HAVE_"):
		continue

	option_value = "%s=%s" % (option, value)
	if not option_value in options:
		if section:
			print
			print "#"
			print "# %s" % section
			print "#"
			section = None

		if value == "n":
			print "# %s is not set" % option
		else:
			print "%s=%s" % (option, value)

f.close()
