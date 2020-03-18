# Notes on installing redis

Install:

`sudo apt-get install redis-server`

Copy config to config location

`sudo cp /home/ubuntu/???/dual_momentum/backend/redis.conf /etc/redis/redis.conf`

Register with systemctl:

`sudo systemctl enable redis-server.service`

Start service

`sudo systemctl restart redis`

Check status:

`sudo systemctl status redis`

Test cli (should return PONG):

`redis-cli ping`



