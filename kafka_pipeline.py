from confluent_kafka import Consumer, Producer, KafkaError
import json
import time
from collections import defaultdict
from datetime import datetime

# Kafka configuration
kafka_conf = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
}

producer_conf = {
    'bootstrap.servers': 'localhost:29092'
}

# Define the consumer and producer
consumer = Consumer(kafka_conf)
producer = Producer(producer_conf)

# Subscribe to the input topic
consumer.subscribe(['user-login'])

# Data structures for insights
locale_insights = defaultdict(lambda: {
    'device_type_count': defaultdict(int),
    'app_version_count': defaultdict(int),
    'login_frequency': defaultdict(int)
})

def process_message(message):
    data = json.loads(message.value().decode('utf-8'))
    
    locale = data.get('locale')
    device_type = data.get('device_type')
    app_version = data.get('app_version')
    timestamp = data.get('timestamp')
    
    if locale:
        insights = locale_insights[locale]
        if device_type:
            insights['device_type_count'][device_type] += 1
        if app_version:
            insights['app_version_count'][app_version] += 1
        if timestamp:
            hour_bucket = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:00:00')
            insights['login_frequency'][hour_bucket] += 1

    # Add a processed timestamp
    data['processed_timestamp'] = int(time.time())
    
    return json.dumps(data)

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            elif msg.error().code() == KafkaError.OFFSET_OUT_OF_RANGE:
                print("Offset out of range, resetting to the earliest offset")
                consumer.seek_to_beginning(consumer.assignment())
                continue
            else:
                print(msg.error())
                break

        processed_message = process_message(msg)
        if processed_message:
            producer.produce('processed-user-login', value=processed_message)
            producer.flush()

except KeyboardInterrupt:
    pass
finally:
    consumer.close()

    # Output the insights grouped by locale
    for locale, insights in locale_insights.items():
        print(f"\nLocale: {locale}")
        print("Device Type Counts:")
        for device_type, count in insights['device_type_count'].items():
            print(f"{device_type}: {count}")

        print("App Version Counts:")
        for app_version, count in insights['app_version_count'].items():
            print(f"{app_version}: {count}")

        print("Login Frequency (Hourly):")
        for hour, count in insights['login_frequency'].items():
            print(f"{hour}: {count}")
