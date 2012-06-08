#!/bin/bash

last=${1}

vim_version="7.3"
vim_url="ftp://ftp.vim.org/pub/vim/patches/${vim_version}"

filenames="${vim_version}.%s.patch0"

for patch in $(seq 1 ${last}); do
	patch=$(printf "${vim_version}.%03d" "${patch}")

	wget -O "vim-${patch}.patch0" "${vim_url}/${patch}"
done
