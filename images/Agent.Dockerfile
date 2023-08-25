FROM docker:dind

ENV AGENT_IMAGE=lightdp-agent
ENV AGENT_VERSION=0.1.0
ENV AGENT_WORKDIR=/opt/lightdp-agent
ENV AGENT_CONTAINER_NAME=lightdp-agent-service
ENV AGENT_LOG_LEVEL=DEBUG

# TODO:

ENTRYPOINT ["/bin/sh", "-c", "dockerd-entrypoint.sh & /your-app/start-command.sh"]