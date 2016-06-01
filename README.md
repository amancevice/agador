# Agador Metaservice for Microservices

<img src="https://travis-ci.org/amancevice/agador.svg?branch=master"/>

Agador is a tool for easily fetching microservice clients using a [consul Key/Value data](https://www.consul.io/intro/getting-started/kv.html) or using its own deployable microservice. With a loaded KV store or a deployed microservice, the agador client can supply a handle to another service.


## Configuration

The agador configuration YAML file defines its services by name and then defines the Python object it will return. An example redis configuration might look like this:

```yaml
redis:
  redis.StrictRedis:
    host: redis.service.com
    port: 6379
    db: 0
```

This defines a service called `"redis"` that will be initialized in Python with:

```python
redis.StrictRedis(host="redis.service.com", port=6379, db=0)
```


## Consul

Consul provides a KV store that can be accessed via `http://<host>:8500/v1/kv/<keys>`. The `consul` module of agador exposes a `load_config()` method that can be used to load a dictionary into the KV store.

```python
config = {
    "redis": {
        "redis.StrictRedis": {
            "host": "redis.service.com",
            "port": 6379,
            "db": 0
        }
    }
}

agador.consul.load_config(config)
```


## Agador Server

If for whatever reason it is not possible to use consul, an agador server can be stood up using the `agador` command and a supplied JSON or YAML configuration URL. Becasue agador uses [furi](https://github.com/amancevice/furi) to parse the URL, the configuration file can be stored locally or on S3.

```bash
agador --config s3://bucket/path/to/config.yaml

# or

agador --config ./config.json
```


## Agador Client

Once an agador service is available through consul or its own service, a Python client can be used to extract a service client for any service defined in the service's configuration.

Example `myservice` usage:

```python
import agador

myservice = agador.service("myservice", host="localhost", port=8500)
# => <MyServiceClient>
```

Agador accepts `ENV` variables as defaults for the agador service location:

* `AGADOR_HOST` the consul or agador host
* `AGADOR_PORT` the consul or agador port
* `AGADOR_SCHEME` http or https
* `AGADOR_KVPATH` the endpoint of the consul KV store (eg, `/v1/kv/agador`)


## Agador example using docker-compose

One potential use case for agador is to stand up a sandboxed local environment where all the services are available locally in a Docker network. A runnable example of this can be found in the [example](./example) directory of this repository.
