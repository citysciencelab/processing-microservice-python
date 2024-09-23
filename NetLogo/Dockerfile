# Start with a base image, e.g., Ubuntu
FROM ubuntu:latest

# Install Python.
RUN apt-get update && apt-get install -y python3 python3-pip wget python3.12-venv

# Install Java.
RUN apt-get install -y default-jdk

# Set environment variables (if necessary)
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH


# Install NetLogo.
ARG NETLOGO_HOME=/opt/netlogo
ARG NETLOGO_VERSION=6.3.0

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    NETLOGO_TARBALL=NetLogo-$NETLOGO_VERSION-64.tgz \
    JAVA_TOOL_OPTIONS=-Xmx4G


ENV NETLOGO_URL=https://ccl.northwestern.edu/netlogo/$NETLOGO_VERSION/$NETLOGO_TARBALL

RUN wget -q $NETLOGO_URL && tar xzf $NETLOGO_TARBALL && ln -sf "NetLogo $NETLOGO_VERSION" netlogo && rm -f $NETLOGO_TARBALL 


# Copy application files into the Docker image
COPY config.py requirements.txt server.py ./app/
COPY ./NetLogo /app/NetLogo
WORKDIR /app

RUN python3 -m venv /app
RUN . /app/bin/activate

RUN /app/bin/pip3 install -r requirements.txt
RUN /app/bin/pip3 install -r NetLogo/requirements.txt

CMD ["/app/bin/python3", "server.py"]