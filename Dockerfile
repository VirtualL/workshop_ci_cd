# Eliran Turgeman
FROM python:3.11.2-slim-buster

# set the working directory
WORKDIR  /boto

# copy the folder wheres the dockerfile
COPY ./main.py .
COPY requirements.txt .

# install the dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

RUN pwd
RUN ls

# run the command to start the app
CMD ["python3", "main.py"]