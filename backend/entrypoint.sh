#!/bin/sh

set -e
mkdir -p /root/.ssh

if [ -f /run/ansible-ssh/id_ed25519 ]; then
  install -m 600 /run/ansible-ssh/id_ed25519 /root/.ssh/id_ed25519
fi

exec "$@"