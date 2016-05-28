import agador

influx = agador.service("influxdb", host="agador")
dynamo = agador.service("dynamodb", host="agador")

print influx
print dynamo
