#!/usr/bin/python
###############################################################################
# IPFire.org    - An Open Source Firewall Solution                            #
# Copyright (C) - IPFire Development Team <info@ipfire.org>                   #
###############################################################################

import re
import sys

filelist = sys.argv[1:]

lines = []
options_state   = {}
options_counter = {}

first_file = True
for filename in filelist:
	f = open(filename)

	for line in f.readlines():
		# Strip newline.
		line = line.rstrip()

		if line.startswith("# Automatically generated file;"):
			continue

		if line.endswith("Kernel Configuration"):
			continue

		if line.startswith("# Compiler:"):
			continue

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

			try:
				options_counter[option_value] += 1
				continue

			except KeyError:
				options_counter[option_value] = 1

		if first_file:
			lines.append(line)

	f.close()
	first_file = False

for line in lines:
	m = re.match("^# (.*) is not set$", line)
	if m:
		if options_counter.get("%s=n" % m.group(1), 0) == len(filelist):
			print "# %s is not set" % m.group(1)

		continue

	m = re.match("^(.*)=(.*)$", line)
	if m:
		if options_counter.get(m.group(0), 0) == len(filelist):
			print m.group(0)

		continue

	print line
