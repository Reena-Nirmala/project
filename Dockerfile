FROM ubuntu:20.04
 
# Avoid interactive prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive
 
# Install Python, pip, and OpenJDK 8 using apt
RUN apt-get update && \
    apt-get install -y python3.9 python3.9-distutils python3.9-venv python3-pip openjdk-8-jdk
 
# Set the working directory
WORKDIR /dj
 
# Copy requirements.txt to the container at /app
COPY requirements.txt requirements.txt
 
# Install Python dependencies
RUN pip3 install -r requirements.txt
 
# Copy the current directory contents into the container at /app
COPY . .
 
# Make port 8000 available to the world outside this container
EXPOSE 8000
 
# Define environment variable for Java
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH
 
# Run your application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8002"]
