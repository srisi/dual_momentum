FROM python:3.7

RUN mkdir   /usr/local/dual_momentum
WORKDIR     /usr/local/dual_momentum
RUN git clone https://github.com/srisi/dual_momentum.git /usr/local/dual_momentum

#RUN pip install -r /usr/local/dual_momentum/requirements.txt
RUN python setup.py install
