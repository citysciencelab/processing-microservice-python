# Start with a base image, e.g., Ubuntu
FROM ubuntu:latest

# Install Python.
RUN apt-get update && apt-get install -y python3 python3-pip wget

# Copy application files into the Docker image
COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install -r Mesa/requirements.txt

CMD ["python3", "server.py"]