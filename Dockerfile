# First stage: Build dependencies

# FROM openjdk:11-jre-slim
# WORKDIR /django
# COPY . /django
# CMD ["java", "-jar", "your-application.jar"]

# FROM python:3.9-slim AS builder
# WORKDIR /django
# COPY requirements.txt requirements.txt
# RUN pip install --upgrade pip && \
#     pip install --no-cache-dir --no-deps -r requirements.txt

# FROM python:3.9-slim
# WORKDIR /django
# COPY . .
# RUN pip install --no-cache -r requirements.txt

# ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8002"]

# First stage: Build dependencies
FROM python:3.9-slim AS builder

WORKDIR /django

# Copy only the requirements file
COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --no-deps -r requirements.txt

# Second stage: Final image with Python and OpenJDK 8
FROM python:3.9-slim

# Install OpenJDK 8
RUN apt-get update && apt-get install -y \
    openjdk-8-jre \
    openjdk-8-jdk

# Set the JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

# Set the working directory in the container
WORKDIR /django

# Copy the application code from the builder stage
COPY . .

# Install any dependencies directly
RUN pip install --no-cache -r requirements.txt

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8002"]



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
