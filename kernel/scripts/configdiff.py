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

printed_sections = []
section = None
for line in f.readlines():
	line = line.rstrip()

	# Ignore some stuff
	if not line or line == "#":
		continue

	if line.startswith("# Automatically generated file;"):
		continue

	if line.endswith("Kernel Configuration"):
		continue

	# End of section
	m = re.match("# end of (.*)$", line)
	if m:
		_section = m.group(1)

		if _section in printed_sections:
			print "# end of %s" % _section

		continue

	# New section
	m = re.match("^# (.*)$", line)
	if m and not "CONFIG_" in line:
		section = m.group(1)
		continue

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
		if section and not section in printed_sections:
			print
			print "#"
			print "# %s" % section
			print "#"
			printed_sections.append(section)

		if value == "n":
			print "# %s is not set" % option
		else:
			print "%s=%s" % (option, value)

f.close()
