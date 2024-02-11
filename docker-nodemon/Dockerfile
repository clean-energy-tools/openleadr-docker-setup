FROM python:3.8

VOLUME /setup
VOLUME /openleadr-python
VOLUME /app

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get update && \
        apt-get upgrade -y && \
        apt-get install -y nodejs build-essential curl locales libffi-dev

RUN npm install -g nodemon
COPY requirements.txt /setup/requirements.txt

RUN pip3 install -r /setup/requirements.txt

COPY nodemon.json /setup/nodemon.json

# CMD nodemon --config /setup/nodemon.json
CMD nodemon --watch /app --watch /openleadr-python \
            --exec python3 /app/app.py

