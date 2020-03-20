FROM python:3.7

#RUN apt update && apt install python3.7 -y

RUN mkdir   /usr/local/dual_momentum
WORKDIR     /usr/local/dual_momentum
COPY . /usr/local/dual_momentum



#RUN cp /usr/local/dual_momentum/backend/redis.conf /etc/redis.conf


#RUN git clone https://github.com/srisi/dual_momentum.git /usr/local/dual_momentum
#RUN git checkout kubernetes

RUN python setup.py install


