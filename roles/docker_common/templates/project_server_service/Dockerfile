FROM debian:latest

RUN apt-get update
RUN apt-get install -y curl apache2 net-tools jq iputils-ping ca-certificates

RUN mkdir -p /etc/apt/keyrings && chmod 755 /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
RUN chmod a+r /etc/apt/keyrings/docker.asc
RUN echo \
	"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
	$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
 	tee /etc/apt/sources.list.d/docker.list > /dev/null

RUN apt-get update
RUN apt-get install -y docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

RUN cd /bin && curl -o coredns_linux_amd64.tgz -L https://github.com/coredns/coredns/releases/download/v1.14.1/coredns_1.14.1_linux_amd64.tgz && tar xzf coredns_linux_amd64.tgz

COPY ./project_server /bin/

RUN mkdir -p /www/

COPY index.cgi /www/

ENTRYPOINT ["/bin/project_server", "entrypoint"]

