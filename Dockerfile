FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y python3.9 python3.9-distutils python3.9-venv python3-pip openjdk-8-jdk
 #
WORKDIR /dj
 
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .
 
EXPOSE 8002

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8002"]
