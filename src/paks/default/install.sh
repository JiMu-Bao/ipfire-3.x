#!/bin/bash
. /opt/pakfire/lib/functions.sh

extract_files

start_service --delay 60 --background ${NAME}
