#!/bin/bash

version=${1}

if [ -z "${version}" ]; then
	echo >&2 "No version!"
	exit 1
fi

export_dir="netpbm-${version}"
rm -rf ${export_dir}

set -x

svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/advanced ${export_dir}
svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/userguide ${export_dir}/userguide
svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/trunk/test ${export_dir}/test
find ${export_dir} -name "\.svn" -type d -print0 | xargs -0 rm -rvf

# removing the ppmtompeg code, due to patents
rm -rf ${export_dir}/converter/ppm/ppmtompeg/

tar cfz netpbm-${version}.tar.gz ${export_dir}
rm -rf ${export_dir}

exit 0
