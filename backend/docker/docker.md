#Docker Setup

#### Dockerfile setup:
see here: https://runnable.com/docker/python/dockerize-your-python-application

make docker available to local user, not just sudo <br>
`sudo groupadd docker`<br>
`sudo usermod -aG docker ${USER}`<br>
`su -s ${USER}`

check that the following command can be run:<br>
`docker run hello-world`


Example:
```
FROM python:3.7

COPY .  /usr/local/dual_momentum

RUN pip install -r /usr/local/dual_momentum/requirements.txt
RUN python /usr/local/dual_momentum/setup.py install
```

Build with <br>
`docker build -t dual_momentum_docker .`

See available images<br>
`docker images`

Run interactive bash session<br>
(-it -> interactive session. --rm remove on exit. bash -> drop in bash shell)<br>
`docker run -it --rm dual_momentum_docker bash`


Delete all images
`docker rmi -f $(docker images -a -q)`
