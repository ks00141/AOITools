from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('datastudy',
                         bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         consumer_timeout_ms=1000)
count = 0

with open(f'./test/test.json', 'w', encoding='utf-8') as file:
    for msg in consumer:
        data = msg.value.decode('utf-8')
        data_parse = json.loads(data)
        json.dump(data_parse, file)
    count += 1
print(count)


