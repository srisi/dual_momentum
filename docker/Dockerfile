# Running gunicor requires opening port 8000
# run with docker run -p 8000:8000 <image> (specify port)
# nginx is on port 80

# image with both python and node
FROM nikolaik/python-nodejs:python3.8-nodejs10

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential \
        curl \
        git \
        libssl-dev \
        nodejs \
        nginx \
        openssl \
        python3-venv

# create new venv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
# add /app to pythonpath (app is where we'll put the repo. trying python setup.py install
# led to errors
ENV PATH="$VIRTUAL_ENV/bin:$PATH" \
    PYTHONPATH=$PYTHONPATH:/app
# redis can't access localhost and instead has to use the docker-compose name
# (e.g. data_redis) as host name. this env var helps to figure out the current environment
ENV RUNNING_IN_DOCKER true
# settings file is in a non-standard place -> set env var
ENV DJANGO_SETTINGS_MODULE config.settings.dev

RUN mkdir -p /app
RUN git clone https://github.com/srisi/dual_momentum.git /app

# build react files
WORKDIR /app/frontend
RUN npm install \
    && npm audit fix \
    && npm update \
    && npm run build

# install django project and create static files
WORKDIR /app/
RUN pip install -r requirements.txt \
    && python backend/manage.py collectstatic \
    && python backend/manage.py migrate

# set working dir to backend where manage.py lives so gunicorn can find it
WORKDIR /app/backend

CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8000", "config.wsgi:application"]
# CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]
