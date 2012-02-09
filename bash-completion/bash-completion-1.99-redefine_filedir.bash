# This is a copy of the _filedir function in bash_completion, included
# and (re)defined separately here because some versions of Adobe
# Reader, if installed, are known to override this function with an
# incompatible version, causing various problems.
#
# https://bugzilla.redhat.com/677446
# http://forums.adobe.com/thread/745833

_filedir()
{
    local i IFS=$'\n' xspec

    _tilde "$cur" || return 0

    local -a toks
    local quoted tmp

    _quote_readline_by_ref "$cur" quoted
    toks=( $(
        compgen -d -- "$quoted" | {
            while read -r tmp; do
                # TODO: I have removed a "[ -n $tmp ] &&" before 'printf ..',
                #       and everything works again. If this bug suddenly
                #       appears again (i.e. "cd /b<TAB>" becomes "cd /"),
                #       remember to check for other similar conditionals (here
                #       and _filedir_xspec()). --David
                printf '%s\n' $tmp
            done
        }
    ))

    if [[ "$1" != -d ]]; then
        # Munge xspec to contain uppercase version too
        # http://thread.gmane.org/gmane.comp.shells.bash.bugs/15294/focus=15306
        xspec=${1:+"!*.@($1|${1^^})"}
        toks+=( $( compgen -f -X "$xspec" -- $quoted ) )
    fi

    # If the filter failed to produce anything, try without it if configured to
    [[ -n ${COMP_FILEDIR_FALLBACK:-} && \
        -n "$1" && "$1" != -d && ${#toks[@]} -lt 1 ]] && \
        toks+=( $( compgen -f -- $quoted ) )

    if [[ ${#toks[@]} -ne 0 ]]; then
        # 2>/dev/null for direct invocation, e.g. in the _filedir unit test
        compopt -o filenames 2>/dev/null
        COMPREPLY+=( "${toks[@]}" )
    fi
} # _filedir()
