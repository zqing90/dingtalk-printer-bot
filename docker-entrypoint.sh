#!/bin/bash -e

echo -e "${ADMIN_PASSWORD}\n${ADMIN_PASSWORD}" | passwd admin

# copy the default config files if they don't exist
if [ ! -f /etc/cups/cupsd.conf ]; then
  cp -rpn /etc/cups-skel/* /etc/cups/
fi

# 后台运行
nohup python /usr/src/app/run.py > printer.log 2>&1 &

exec "$@"

