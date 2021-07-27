FROM jenkins4eval/jenkins
USER root
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y build-essential cmake astyle
RUN apt-get install -y python3 python3-pip
RUN pip3 install virtualenv
USER jenkins
EXPOSE 8080
EXPOSE 50000
ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/jenkins.sh"]
