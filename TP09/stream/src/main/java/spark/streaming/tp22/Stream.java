package spark.streaming.tp22;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Encoders;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.streaming.StreamingQuery;
import org.apache.spark.sql.streaming.StreamingQueryException;
import org.apache.spark.sql.streaming.Trigger;

import java.util.Arrays;
import java.util.concurrent.TimeoutException;

public class Stream {

    public static void main(String[] args) throws StreamingQueryException, TimeoutException {

        SparkSession spark = SparkSession
                .builder()
                .appName("NetworkWordCount")
                .master("local[*]")
                .getOrCreate();

        // قراءة stream من socket localhost:9999
        Dataset<String> lines = spark
                .readStream()
                .format("socket")
                .option("host", "localhost")
                .option("port", 9999)
                .load()
                .as(Encoders.STRING());

        // تقسيم السطور إلى كلمات
        Dataset<String> words = lines.flatMap(
                (String x) -> Arrays.asList(x.split(" ")).iterator(),
                Encoders.STRING()
        );

        // عدّ الكلمات (groupBy + count)
        Dataset<Row> wordCounts = words.groupBy("value").count();

        // طباعة النتائج في الـ console كل ثانية
        StreamingQuery query = wordCounts
                .writeStream()
                .outputMode("complete")
                .format("console")
                .trigger(Trigger.ProcessingTime("1 second"))
                .start();

        query.awaitTermination();
    }
}
