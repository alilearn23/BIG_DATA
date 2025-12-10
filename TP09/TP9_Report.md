# TP9 – Batch and Streaming Data Processing with Apache Hadoop & Apache Spark

## 1. Introduction

This practical session (TP9) focuses on applying **Big Data processing techniques** using **Apache Hadoop** and **Apache Spark**.  
The objectives of the TP include:

- Setting up a working environment using Docker, Hadoop, and Spark  
- Implementing **Batch Processing** using:
  - Scala (Spark Shell)
  - Java (Maven Project)
- Implementing **Streaming Processing** using:
  - Netcat as a streaming data source
  - Spark Structured Streaming for real-time word counting

This report summarizes the steps taken, tools used, and the results obtained during the TP.

---

## 2. Environment Setup

### 2.1 Tools Used
- Docker  
- Apache Hadoop 3.3.6  
- Apache Spark 3.5.0  
- OpenJDK 11  
- Maven 3.9.x  
- Netcat (nc)

### 2.2 Container Setup

A single container used as the master node:

```
docker exec -it hadoop-spark-master bash
```

Inside the container:

- Hadoop installed in: `/root/hadoop`
- Spark installed in: `/root/spark`
- JAVA_HOME configured for OpenJDK 11

---

## 3. Batch Processing Using Spark (Scala)

### 3.1 Creating a Test File

```
cd /root
cat > file1.txt
Hello Spark Wordcount!
Hello Hadoop Also :)
```

### 3.2 Running Spark Shell

```
spark-shell
```

### 3.3 Scala WordCount Code

```scala
val lines = sc.textFile("file1.txt")
val words = lines.flatMap(_.split("\s+"))
val pairs = words.map(word => (word, 1))
val wc = pairs.reduceByKey(_ + _)
wc.collect().foreach(println)
wc.saveAsTextFile("file1.count")
```

### 3.4 Example Output

```
(Hello,2)
(Spark,1)
(Wordcount!,1)
(Hadoop,1)
(Also,1)
```

---

## 4. Batch Processing Using Java + Maven

### 4.1 Creating the Maven Project

```
mvn archetype:generate  -DgroupId=spark.batch  -DartifactId=wordcount-spark  -DarchetypeArtifactId=maven-archetype-quickstart  -DinteractiveMode=false
```

### 4.2 Java WordCount Code

```java
JavaRDD<String> lines = sc.textFile("purchases.txt");
JavaRDD<String> words = lines.flatMap(x -> Arrays.asList(x.split(" ")).iterator());
JavaPairRDD<String, Integer> pairs = words.mapToPair(s -> new Tuple2<>(s, 1));
JavaPairRDD<String, Integer> wc = pairs.reduceByKey((a, b) -> a + b);
wc.saveAsTextFile("out-java-local");
```

### 4.3 Packaging and Running

```
mvn clean package
docker cp target/wordcount-spark-1.0-SNAPSHOT.jar hadoop-spark-master:/root/
spark-submit --class spark.batch.App wordcount-spark.jar
```

Output saved in:

```
out-java-local/
```

---

## 5. Streaming Processing (Structured Streaming)

### 5.1 Creating Maven Project

```
mvn archetype:generate  -DgroupId=spark.streaming  -DartifactId=stream-tp9  -DarchetypeArtifactId=maven-archetype-quickstart  -DinteractiveMode=false
```

### 5.2 Key Dependencies

```xml
<dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-core_2.12</artifactId>
    <version>3.5.0</version>
</dependency>
<dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-sql_2.12</artifactId>
    <version>3.5.0</version>
</dependency>
```

### 5.3 Streaming Java Code

```java
SparkSession spark = SparkSession
        .builder()
        .appName("NetworkWordCount")
        .master("local[*]")
        .getOrCreate();

Dataset<String> lines = spark
        .readStream()
        .format("socket")
        .option("host", "localhost")
        .option("port", 9999)
        .load()
        .as(Encoders.STRING());

Dataset<String> words = lines.flatMap(
        (String x) -> Arrays.asList(x.split(" ")).iterator(),
        Encoders.STRING()
);

Dataset<Row> wordCounts = words.groupBy("value").count();

StreamingQuery query = wordCounts
        .writeStream()
        .outputMode("complete")
        .format("console")
        .trigger(Trigger.ProcessingTime("1 second"))
        .start();

query.awaitTermination();
```

### 5.4 Running the Streaming Job

#### Terminal 1 – Start Netcat:

```
nc -lk 9999
```

Type messages:

```
hello spark
hello streaming
spark spark
```

#### Terminal 2 – Run Spark Streaming:

```
spark-submit --class spark.streaming.tp22.Stream --master local stream-1.jar > out
```

### 5.5 Example Output

```
-------------------------------------------
Batch: 1
+-----------+-----+
| value     |count|
+-----------+-----+
| hello     | 2   |
| spark     | 3   |
| streaming | 1   |
+-----------+-----+
```

Output stored in:

```
/root/out
```

---

## 6. Conclusion

This TP demonstrated:

- Batch processing using Spark (Scala + Java)
- Interaction with Hadoop HDFS
- Real-time processing with Spark Structured Streaming
- Use of Docker to manage the environment
- Maven for packaging and deployment

A complete data-processing pipeline was created, covering offline and real-time analytics.

---

# End of Report
