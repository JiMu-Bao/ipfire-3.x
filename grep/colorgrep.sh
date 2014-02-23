# color-grep initialization

if [ -r /etc/GREP_COLORS ]; then
	grep -qi "^COLOR.*none" /etc/GREP_COLORS >/dev/null 2>/dev/null && return
fi

alias grep='grep --color=auto' 2>/dev/null
alias egrep='egrep --color=auto' 2>/dev/null
alias fgrep='fgrep --color=auto' 2>/dev/null
