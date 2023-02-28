# Follow the practice introduced in 
# https://github.com/kubeflow/kubeflow/tree/master/components/example-notebook-servers/
ARG BASE_IMG=<base>
FROM $BASE_IMG

WORKDIR /
ENV NB_USER vitis-ai-user
ARG KUBECTL_ARCH="amd64"
ARG KUBECTL_VERSION=v1.21.0
ARG S6_ARCH="amd64"
ARG S6_VERSION=v2.2.0.3
RUN export GNUPGHOME=/tmp/ \
    && curl -sL "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-${S6_ARCH}-installer" -o /tmp/s6-overlay-${S6_VERSION}-installer \
    && chmod +x /tmp/s6-overlay-${S6_VERSION}-installer \
    && /tmp/s6-overlay-${S6_VERSION}-installer / \
    && rm /tmp/s6-overlay-${S6_VERSION}-installer
RUN curl -sL "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${KUBECTL_ARCH}/kubectl" -o /usr/local/bin/kubectl \
    && curl -sL "https://dl.k8s.io/${KUBECTL_VERSION}/bin/linux/${KUBECTL_ARCH}/kubectl.sha256" -o /tmp/kubectl.sha256 \
    && echo "$(cat /tmp/kubectl.sha256) /usr/local/bin/kubectl" | sha256sum --check \
    && rm /tmp/kubectl.sha256 \
    && chmod +x /usr/local/bin/kubectl
RUN chown -R vitis-ai-user:vitis-ai-group /usr/local/bin \
    && chown -R vitis-ai-user:vitis-ai-group /etc/s6
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ARG CODESERVER_VERSION=v4.3.0
RUN curl -sL "https://github.com/cdr/code-server/releases/download/${CODESERVER_VERSION}/code-server_${CODESERVER_VERSION/v/}_amd64.deb" -o /tmp/code-server.deb \
    && dpkg -i /tmp/code-server.deb \
    && rm -f /tmp/code-server.deb
COPY --chown=vitis-ai-user:vitis-ai-group docker/s6/ /etc
USER vitis-ai-user
EXPOSE 8888
ENTRYPOINT ["/init"]