# Eliran Turgeman
# Build (Stage1)
FROM python:3.11.2 as builder
# PYTHONUNBUFFERED Force logging to stdout / stderr not to be buffered into ram  
ENV PYTHONUNBUFFERED=1 
# set the working directory
WORKDIR  /boto
# copy the folder wheres the dockerfile
COPY ./main.py .
WORKDIR /wheels
COPY requirements.txt .
# PIP Will create an archive of our libraries so we don't need to download them again
# argument - wheel
RUN pip wheel -r ./requirements.txt 

# Unit Tests (stage-2)
#FROM python:3.6 as unit-tests
#WORKDIR /usr/src/app
# Copy all packages instead of rerunning pip install
#COPY --from=builder /wheels /wheels
#RUN     pip install -r /wheels/requirements.txt \
                      #-f /wheels \
       #&& rm -rf /wheels \
       #&& rm -rf /root/.cache/pip/* 

#COPY --from=builder /usr/src/app/ ./
#RUN ["make", "test"]

# lint (stage-2)
FROM eeacms/pylint:latest as linting
WORKDIR /code
# COPY --from=builder /boto/pylint.cfg /etc/pylint.cfg
COPY --from=builder /boto/*.py ./
RUN ["/docker-entrypoint.sh", "pylint"]


# RUN (Stage 3) Starts the python app
FROM python:3.11.2-slim as run
WORKDIR /boto
# Copy all packages instead of rerunning pip install
COPY --from=builder /wheels /wheels
RUN     pip install -r /wheels/requirements.txt \
                     -f /wheels \
       && rm -rf /wheels \
       && rm -rf /root/.cache/pip/* 

COPY --from=builder /boto/*.py ./
#CMD ["python", "run_app.py"]
# run the command to start the app
CMD ["python3", "main.py"]