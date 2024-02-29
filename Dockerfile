FROM python:3.11.6-alpine3.18 

# setup environment variable  
ENV DockerHOME=/home/app/webapp  

# set work directory  
RUN mkdir -p $DockerHOME  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies 
RUN pip3 install --upgrade setuptools 
RUN python -m pip install --upgrade pip

# copy whole project to your docker home directory. 
COPY . $DockerHOME  

# run this command to install all dependencies  
RUN pip install -r requirements.txt  

# port where the Django app runs  
EXPOSE 8000  

# Use the entrypoint script as the CMD instruction
CMD ["/bin/sh", "/home/app/webapp/django_run.sh"]