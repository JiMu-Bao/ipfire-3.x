#!/bin/bash
###############################################################################
#                                                                             #
# IPFire.org - A linux based firewall                                         #
# Copyright (C) 2007, 2008, 2009 Michael Tremer & Christian Schmidt           #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                             #
###############################################################################
#

NAME="IPFire"                       # Software name
SNAME="ipfire"                      # Short name
VERSION="3.0-prealpha2"             # Version number
SLOGAN="Gluttony"                   # Software slogan

BASEDIR=/ipfire-3.x

. ${BASEDIR}/tools/ui-functions

NAOKI=${BASEDIR}/tools/naoki

while [ $# -gt 0 ]; do
	case "${1}" in
		--debug|-d)
			DEBUG=1
			log DEBUG "Debugging mode enabled by command line."
			;;
		*)
			action=${1}
			shift
			break
			;;
	esac
	shift
done

function package() {
	local action=${1}
	shift

	case "${action}" in
		dependencies|deps)
			echo -e "${BOLD}Build dependencies:${NORMAL} $(package_build_dependencies $@)"
			echo -e "${BOLD}Dependencies:${NORMAL}       $(package_dependencies $@)"
			;;
		find)
			find_package $@
			;;
		list)
			${NAOKI} --toolchain list
			;;
		profile|info)
			${NAOKI} profile $@
			;;
		_info)
			package_info $(find_package $@)
			;;
	esac
}

function listmatch() {
	local arg=${1}
	shift
	
	local value
	for value in $@; do
		if [ "${arg}" == "${value}" ]; then
			return 0
		fi
	done
	return 1
}


case "${action}" in
	package|pkg)
		package $@
		;;
	toolchain)
		TOOLCHAIN=1
		${NAOKI} --toolchain tree
		;;
	toolchain_build)
		for i in $($0 toolchain); do
			${NAOKI} --toolchain toolchain ${i}
		done
		;;
	tree)
		${NAOKI} tree
		;;
esac
