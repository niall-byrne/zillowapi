FROM python:3.7-slim
MAINTAINER niall@niallbyrne.ca
LABEL PROJECT=zillowapi

ENV PYTHONUNBUFFERED 1

# Mark Container
RUN echo "zillow" > /etc/container_release

# Install Dependencies
RUN apt-get update      && \
    apt-get upgrade -y  && \
    apt-get install -y     \
    bash                   \
    build-essential        \
    jq                     \
    libpq-dev              \
    openssh-client         \
    postgresql-client      \
    shellcheck             \
    sudo                   \
    tig                    \
    vim

# Setup directories
RUN mkdir -p /home/user /app
WORKDIR /app

# Copy codebase and bash environment
COPY . /app
COPY development/bash /home/user/

# Create the runtime user, and change permissions
RUN useradd user -d /home/user        \
                 -s /bin/bash         \
                 -M                   \
 && chown -R user:user /home/user     \
 && chown -R user:user /app           \
 && echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER user

# Setup The Dev CLI
RUN scripts/commander.sh setup
