FROM debian:latest

ARG http_proxy
ARG https_proxy

# Install docker
RUN apt-get update
RUN apt-get -y remove docker docker-engine docker.io containerd runc || true
RUN apt-get -y install ca-certificates curl gnupg lsb-release
RUN mkdir -p /etc/apt/keyrings
RUN curl -kfsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update
RUN apt-get -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install other packages
RUN apt-get install -y ssh net-tools systemd python3

# removing unused systemd services
RUN rm -f /lib/systemd/system/*.mount && \
    rm -f /lib/systemd/system/*.path && \
    rm -f /lib/systemd/system/*.swap && \
    rm -f /lib/systemd/system/*.wants/*.mount && \
    rm -f /lib/systemd/system/*.wants/*.path && \
    rm -f /lib/systemd/system/*.wants/*.swap && \
    rm -f /lib/systemd/system/systemd-sysctl.service && \
    rm -f /lib/systemd/system/systemd-update-utmp.service

RUN echo "UseDNS no\nKerberosAuthentication no\nGSSAPIAuthentication no\nPermitRootLogin yes\n" >> /etc/ssh/sshd_config

RUN echo "root:password" | chpasswd

RUN systemctl enable ssh

STOPSIGNAL SIGRTMIN+5

CMD ["/usr/sbin/init"]