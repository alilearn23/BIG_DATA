# 🔧 TP N°7 Report  
## Apache Kafka using Docker & Python

**🎓 Student:** Ali Lakhoues  
**📅 Date:** 23/11/2025  
**💻 System:** Windows 10/11 — Docker Desktop — Python 3.11

---

## 🧩 Part 1: Setup Kafka (Single Broker)

### 📁 docker-compose.yml
```yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.3.2
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.3.2
    container_name: kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:29092,PLAINTEXT_HOST://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

### ▶️ Start containers
```powershell
docker-compose up -d
docker ps
```

---

## 🧪 Part 2: CLI Test (Producer & Consumer)

### 📌 Create Topic
```powershell
docker exec -it kafka /bin/bash
kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 📩 Run Consumer
```powershell
docker exec -it kafka /bin/bash
kafka-console-consumer --topic test-topic --bootstrap-server localhost:9092
```

### 📤 Run Producer
```powershell
docker exec -it kafka /bin/bash
kafka-console-producer --topic test-topic --bootstrap-server localhost:9092
# Example message: Hello Kafka 🚀
```

---

## 🚨 Part 3: IoT Simulation (Python)

### 📦 Install dependency
```powershell
pip install kafka-python
```

### 🛰 sensor.py (Producer)
```python
import time, json, random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

machine = "Machine-A1"
print(f"✅ Sensor activated for {machine}...")

while True:
    temp = random.randint(15, 110)
    payload = {"device": machine, "temp": temp, "time": time.time()}
    producer.send("sensor-data", value=payload)
    print(f"📤 Sent → {payload}")
    time.sleep(2.5)
```

### 📡 monitor.py (Consumer)
```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "sensor-data",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("✅ Monitoring system running... 🔥")

for msg in consumer:
    t = msg.value["temp"]
    if t > 85:
        print(f"⚠️ HIGH TEMP ALERT! Overheating: {t}°C 🚒")
    elif t < 0:
        print(f"❄ Low temperature detected: {t}°C")
    else:
        print(f"✔ Normal reading: {t}°C")
```

### ▶️ Run scripts
```powershell
python sensor.py
python monitor.py
```

---

## 🧱 Part 4: Kafka Cluster (2 Brokers)

### ♻️ Reset env
```powershell
docker-compose down --volumes --remove-orphans
```

### 📁 docker-compose.yml (Cluster)
```yaml
version: "3.8"
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.3.2
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka1:
    image: confluentinc/cp-kafka:7.3.2
    container_name: kafka1
    depends_on: [zookeeper]
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka1:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTTEXT:PLAINTEXIT,PLAINTTEXT_HOST:PLAINTTEXT
      KAFKA_INTER_BROKER_LISTENAME: PLAINTEX
      KAFKA_OFFSETS_TOPIC_REPLICATIONFACTOR: 2

  kafka2:
    image: confluentinc/cp-kafka:7.3.2
    container_name: kafka2
    depends_on: [zookeeper]
    ports:
      - "9093:9093"
    environment:
      KAFKA_BROKER_ID: 2
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXIT://kafka2:29092,PLAINTEXT_HOST://localhost:9093
      KAFKA_LISTENER_SECURITYPROTO_MAP: PLAINTEXIT:PLAINTEDIA,PLAINTEXIT_HOST:PLAINTEXIT
      KAFKA_INTERBROKER_LISTENNAME: PLAINTEX
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 2
```

### ▶️ Start cluster
```powershell
docker-compose up -d
```

### 💾 Create replicated topic
```powershell
docker exec -it kafka1 /bin/bash
kafka-topics --create --topic backup-stream --bootstrap-server localhost:9092 --partitions 1 --replication-factor 2
kafka-topics --describe --topic backup-stream --bootstrap-server localhost:9092
# Expected result: Replicas → 1,2 ✅
```

---

## ✅ Final Results
- Kafka Docker Deployment ✅  
- CLI Producer/Consumer ✅  
- Python IoT Pipeline ✅  
- Cluster Replication ✅  

---

**📌 Report generated automatically**
