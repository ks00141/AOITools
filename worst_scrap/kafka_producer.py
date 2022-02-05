def kafka_producer(producer, data, server_ip, topic):
    producer = producer(bootstrap_servers=server_ip)
    producer.send(topic=topic,
                  value=data.encode('UTF-8'))
