# Leaves PATH unchanged if icecc is already there.
# If ccache is there, adds icecc _after_ it.
# Otherwise adds icecc to the beginning.

PATH=`echo $PATH | /bin/sed -e \
	'\%@LIBDIR@/icecc/bin% b
	s%@LIBDIR@/ccache%&:@LIBDIR@/icecc/bin%
	t
	s%^%@LIBDIR@/icecc/bin:%'`

