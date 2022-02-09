from kafka import KafkaConsumer


def kafka_consumer(consumer, server_ip, topic):
    consumer = consumer(bootstrap_servers=server_ip)
    consumer.subscribe(topic)
    for msg in consumer:
        print(msg)


kafka_consumer(consumer=KafkaConsumer,
               server_ip='localhost:9092',
               topic='PST')

