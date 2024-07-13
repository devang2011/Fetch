# Real-Time Streaming Data Pipeline with Kafka and Docker

This project sets up a real-time streaming data pipeline using Kafka and Docker. The pipeline ingests streaming data, processes it in real-time, and stores the processed data into a new Kafka topic.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Pipeline](#running-the-pipeline)
- [Stopping the Pipeline](#stopping-the-pipeline)
- [Design Choices and Data Flow](#design-choices-and-data-flow)


## Prerequisites

1. **Docker**: Ensure Docker is installed on your local machine. You can download it from [here](https://www.docker.com/get-started).
2. **Python**: Make sure Python is installed. You can download it from [here](https://www.python.org/downloads/).
3. **Kafka Python Client**: Install the Kafka Python client library using the following command:
   ```sh
   pip install confluent_kafka

## Setup
1. **Clone the Repository**:
   ```sh
   git clone <repository_url>
   cd <repository_directory>

2. **Docker Compose File**:
Ensure you have the following docker-compose.yml file in your project directory

3. **Start Docker Containers**:
   Start the containers using Docker Compose:
   ```sh
   docker-compose up -d

4. **Create Kafka Topics**:
   Ensure the following Kafka topics are created:
   Make sure to replace <kafka_container_id> with actual ID
   ```sh
   docker exec -it <kafka_container_id> kafka-topics --create --topic user-login --bootstrap-server localhost:29092 --replication-factor 1 --partitions 1
   docker exec -it <kafka_container_id> kafka-topics --create --topic processed-user-login --bootstrap-server localhost:29092 --replication-factor 1 --partitions 1
## Running the Pipeline

1. **Create a Kafka Consumer Script**:

   Ensure the script `kafka_pipeline.py` is present in project directory

2. **Run the script**:
   Execute the following command to start the Kafka consumer script:

   ```sh
   python kafka_pipeline.py

## Stopping the Pipeline

1. **Stop the Kafka Consumer Script**:
   Press `Ctrl+C` in the terminal where the script is running. This will stop the script and output the insights collected so far.

2. **Stop Docker Containers**:
   To stop the Docker containers, run the following command:
   ```sh
   docker-compose down

## Design Choices and Data Flow

#### Design Choices

1. **Kafka for Real-Time Data Streaming**:
   - Kafka is chosen for its high-throughput, low-latency capabilities, and its support for stream processing and distributed data.
   - Kafka’s topic-partition model allows horizontal scaling, making it suitable for handling large volumes of streaming data.

2. **Docker for Containerization**:
   - Docker ensures that the entire environment (including Kafka, Zookeeper, and the data generator) is consistent across different setups.
   - Using Docker Compose simplifies the setup process and makes it easy to manage multi-container applications.

3. **Python for Data Processing**:
   - Python is chosen for its simplicity and the availability of robust libraries for Kafka integration (e.g., `confluent_kafka`).
   - The Python script is designed to consume, process, and produce messages efficiently.

#### Data Flow

1. **Data Ingestion**:
   - The data generator produces user login events to the `user-login` Kafka topic. Each event contains fields like `user_id`, `app_version`, `device_type`, `ip`, `locale`, `device_id`, and `timestamp`.

2. **Data Consumption**:
   - A Kafka consumer (implemented in Python) subscribes to the `user-login` topic.
   - The consumer polls the topic to fetch batches of messages.

3. **Data Processing**:
   - Each consumed message is parsed from JSON.
   - The message is processed to extract insights such as device type distribution, app version usage, and login frequency grouped by locale.
   - Insights are aggregated in in-memory data structures (using Python’s `defaultdict`).

4. **Data Production**:
   - The processed messages are enriched with a `processed_timestamp` and sent to the `processed-user-login` Kafka topic.
   - This is done asynchronously to ensure high throughput.

5. **Output Insights**:
   - Upon termination (or periodically, depending on implementation), the script outputs the aggregated insights to the console.
