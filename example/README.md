# Agador example using docker-compose

In this example we will start a network with a consul backend, services for InfluxDB and Redis, and an IPython notebook with which to experiment.


## Setup

### Consul

We will bring up a consul agent using the official docker image and run it in `dev` mode under the domain `consul.service.com`:

```yaml
consul:
  image: consul
  hostname: consul
  domainname: service.com
  command: agent -dev -client 0.0.0.0
```


### InfluxDB

Next, we will bring up an InfluxDB node under the domain `influxdb.service.com`

```yaml
influxdb:
  image: influxdb
  hostname: influxdb
  domainname: service.com
```


### Redis

Finally, we will bring up a Redis node under the domain `redis.service.com`

```yaml
redis:
  image: redis
  hostname: redis
  domainname: service.com
```


### Notebook

In order to interact with all our services we will need to create a development environment that has `influxdb`, `redis`, and of course `agador` installed. We will do this with a trivial [`Dockerfile`](./Dockerfile) and include it in our [`docker-compose.yaml`](./docker-compose.yaml). Our client environment will run an IPython notebook and link to our `consul`, `influxdb`, and `redis` nodes.

```yaml
notebook:
  build: .
  command: sh -c "jupyter notebook --ip=* --no-browser"
  ports:
    - "8888:8888"
  volumes:
    - ./example.ipynb:/example/example.ipynb
    - ./example.yaml:/example/example.yaml
  links:
    - consul:consul.service.com
    - influxdb:influxdb.service.com
    - redis:redis.service.com

```


## Starting the network

Start a composed group of containers with:

```bash
docker-compose up
```

Navigate your browser to [http://localhost:8888](http://localhost:8888) to view an IPython notebook sandbox playground

## Clean up

Clean up the environment with:

```bash
docker-compose down --rmi local
```

This will remove the notebook image once the network is down.
