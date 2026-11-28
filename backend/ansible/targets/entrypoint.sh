#!/bin/sh

set -e

mkdir -p /home/ansible/.ssh

if [ -f /run/ansible-ssh/id_ed25519.pub ]; then
  install -o ansible -g ansible -m 600 \
  /run/ansible-ssh/id_ed25519.pub \
  /home/ansible/.ssh/authorized_keys
fi

chown -R ansible:ansible /home/ansible/.ssh
chmod 700 /home/ansible/.ssh
chmod 600 /home/ansible/.ssh/authorized_keys

ssh-keygen -A

exec /usr/sbin/sshd -D -e