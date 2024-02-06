# First stage: Build dependencies
FROM openjdk:11 AS builder

WORKDIR /django

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip

COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir --no-deps -r requirements.txt

# Second stage: Final image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /django

# Copy the application code from the builder stage
COPY . .

# Install Django
RUN pip3 install Django

# Set the PYTHONPATH
ENV PYTHONPATH /django

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8002"]
# First stage: Build dependencies


















# FROM python:3.9 AS builder
# WORKDIR /django
# COPY requirements.txt requirements.txt
# # Install any needed packages specified in requirements.txt
# RUN pip install --upgrade pip && \
#     pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt
# # Second stage of the multi-stage build
# FROM python:3.9-slim
# # Set the working directory in the container
# WORKDIR /django
# # Copy the dependencies and application code from the builder stage
# COPY --from=builder /wheels /wheels
# COPY . .
# # Install any dependencies from the wheels directory
# RUN pip install --no-cache /wheels/*
# ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8002"]
# First stage: Build dependencies
# First stage: Build dependencies

# FROM python:3.9 AS builder

# WORKDIR /django

# COPY requirements.txt requirements.txt

# # Install Python dependencies
# RUN pip install --upgrade pip 

# # Second stage: Runtime environment
# FROM amazonlinux:latest

# # Set the working directory in the container
# WORKDIR /django

# # Copy the dependencies and application code from the builder stage
# COPY --from=builder /django /django
# COPY . .

# # Install Python dependencies from the wheels directory


# # Install Java using yum
# RUN yum install -y java-11-amazon-corretto

# # Set environment variable for Java
# ENV JAVA_HOME /usr/lib/jvm/java-11-amazon-corretto
# ENV PATH $PATH:$JAVA_HOME/bin

# # Remove the /wheels directory

# # Make port 8002 available to the world outside this container
# EXPOSE 8002

# # Define the command to run your application
# ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8002"]
