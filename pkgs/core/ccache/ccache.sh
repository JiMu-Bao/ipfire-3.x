# Use ccache by default.  Users who don't want that can set the CCACHE_DISABLE
# environment variable in their personal profile.

case ":${PATH:-}:" in
    *:@LIBDIR@/ccache:*) ;;
    *) PATH="@LIBDIR@/ccache${PATH:+:$PATH}" ;;
esac

# If @CACHEDIR@ is writable, use a shared cache there.  Users who don't
# want that even if they have that write permission can set the CCACHE_DIR
# and unset the CCACHE_UMASK environment variables in their personal profile.

if [ -z "${CCACHE_DIR:-}" ] && [ -w @CACHEDIR@ ] && [ -d @CACHEDIR@ ] ; then
    export CCACHE_DIR=@CACHEDIR@
    export CCACHE_UMASK=002
    unset CCACHE_HARDLINK
fi

