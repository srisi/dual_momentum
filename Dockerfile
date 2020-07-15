# This Dockerfile defines a container with our dev toolchain preinstalled.
# We expect images to be built with the context directory set to be the root
# directory of repo and using the `-f` flag to specify this Dockerfile.
#
# run with docker run -p 8000:8000 <image> (specify port)

FROM nikolaik/python-nodejs:python3.8-nodejs10 as django-gunicorn

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

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH" \
    PYTHONPATH=$PYTHONPATH:/app
ENV RUNNING_IN_DOCKER true

RUN mkdir -p /app
RUN git clone https://github.com/srisi/dual_momentum.git /app

WORKDIR /app/frontend
RUN npm install \
    && npm audit fix \
    && npm update \
    && npm run build

WORKDIR /app/
RUN pip install -r requirements.txt \
    && python backend/manage.py collectstatic \
    && python backend/manage.py migrate

WORKDIR /app/backend


# CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]


#    && go get golang.org/dl/go1.12.7 \
#    && go1.12.7 download \
#    && go1.12.7 get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway \
#        github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger \
#        github.com/golang/protobuf/protoc-gen-go \
#    && echo 'alias go=go1.12.7' >> ~/.profile \
#    && wget -qO/bin/grpc-health-probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/v0.2.2/grpc_health_probe-linux-amd64 \
#    && chmod +x /bin/grpc-health-probe \
#    && pip3 install --no-cache-dir -r /requirements.txt \
#    && apt-get remove -y git \
#    && apt-get clean \
#    && apt-get autoremove -y \
#    && rm -rf /var/lib/apt/lists/*

# This needs to be set so that we can mount our local directory to /app and run
# commands in our container against files on our host machine.
#COPY . /app
#WORKDIR /app
#
#RUN bin/internal/compile-protos
