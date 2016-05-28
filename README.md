# Agador Metaservice for Microservices

Agador is a microservice for configuring a suite of other microservices. Once deployed with a service configuration, the agador server can supply a client with the information needed to instantiate a client for that particular service.


## Server

The agador server can be stood up using the `agador` command and a supplied JSON or YAML configuration URL. Becasue agador uses [furi](https://github.com/amancevice/furi) to parse the URL, the configuration file can be stored locally or on S3.

Example configuration:

```yaml
--- # Agador Metaervice Configuration
myservice:
  module:
    name: myservice.client
    package: ~
  class: MyClient
  args:
    host: myservice.service.consul
    port: 7777
```

Example server run command:

```bash
agador --config s3://bucket/path/to/config.yaml

# or

agador --config ./config.json
```


## Client

Once an agador service is available, a Python client can be used to extract a service client for any service defined in the service's configuration.

Example `myservice` usage:

```python
import agador

myservice = agador.service("myservice", host="localhost", port=9999)
# => <MyServiceClient>
```


## Agador example using Docker

One potential use case for agador is to stand up a sandboxed local environment where all the services are available locally in a Docker network. A runnable example of this can be found in the [example](./example) directory of this repository.


### Creating a Network

All our containers need to communicate to eachother, so we will create a bridge network called `agador` for them to see one another:

```bash
docker network create --driver bridge agador
```

Once the bridge is created, we can stand up the services one after another:

```bash
docker run --hostname influxdb ...
docker run --hostname dynamodb ...
docker run --hostname agador ...
```


### Building a Client Environment

In this example we will stand up agador with two services and a client using four Docker containers:
* Agador Service
* InfluxDB
* DynamoDB
* Agador Client

Because our client is expected to use InfluxDB and DynamoDB, we should ensure our client envrionment installs the `influxdb` and `boto3` pips. See the example [`Dockerfile`](./example/Dockerfile) to see how this environment is built.


### Consuming services

Once the network and sandbox client environment has been set up, the client is able to consume any of the available services using agador:

```python
import agador

influxdb = agador.service("influxdb", host="agador")
# => <InfluxDBClient>
dynamodb = agador.service("dynamodb", host="agador")
# => dynamodb.ServiceResource()
```


### Running the example

A runnable example is made available in the [example](./example) directory. To use it run the following commands:

```bash
git clone https://github.com/amancevice/agador.git
cd agador/example
./example.sh
```

Output:

```
Building example client Docker image
Creating agador docker bridge network
Starting influxdb
Starting dynamodb
Starting agador with config:

--- # Agador Metaervice Configuration
influxdb:
  module:
    name: "influxdb"
  class: "InfluxDBClient"
  args:
    host: "influxdb.service.consul"
    port: 8086

dynamodb:
  module:
    name: "boto3"
  class: "resource"
  args:
    service_name: "dynamodb"
    endpoint_url: "http://dynamodb:8000/"
    region_name: "us-east-1"

Running example Python:

import agador

influx = agador.service("influxdb", host="agador")
dynamo = agador.service("dynamodb", host="agador")

print influx
print dynamo

Output:

<influxdb.client.InfluxDBClient object at 0x7f7f781abfd0>
dynamodb.ServiceResource()

Cleaning up
```
