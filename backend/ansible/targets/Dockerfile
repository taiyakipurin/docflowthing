FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    python3 \
    sudo \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ansible \
    && mkdir -p /home/ansible/.ssh \
    && mkdir -p /var/run/sshd \
    && chown -R ansible:ansible /home/ansible/.ssh \
    && chmod 700 /home/ansible/.ssh/ \
    && echo "ansible ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ansible \
    && chmod 440 /etc/sudoers.d/ansible


COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]