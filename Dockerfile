# Use an official Python runtime as a parent image
FROM python:3.9 AS builder
 
# Set the working directory in the container
WORKDIR /django
 
# Copy the requirements file into the container at /django
COPY requirements.txt requirements.txt
 
# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt
 
# Second stage of the multi-stage build
FROM python:3.9-slim
 
# Set the working directory in the container
WORKDIR /django
 
# Copy the dependencies and application code from the builder stage
COPY --from=builder /wheels /wheels
COPY . .
 
# Install any dependencies from the wheels directory
RUN pip install --no-cache /wheels/*
 
# Make port 8002 available to the world outside this container
 
# Define the command to run your application
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8002"]
