package spark.batch.tp21;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import scala.Tuple2;

import java.util.Arrays;

public class WordCountTask {

    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: WordCountTask <inputPath> <outputDir>");
            System.exit(1);
        }

        String inputPath = args[0];
        String outputDir = args[1];

        new WordCountTask().run(inputPath, outputDir);
    }

    public void run(String inputPath, String outputDir) {
        // ملاحظة: لا نضبط setMaster هنا، نخليها لـ spark-submit (--master ...)
        SparkConf conf = new SparkConf()
                .setAppName("WordCountTask");

        JavaSparkContext sc = new JavaSparkContext(conf);

        // قراءة الملف (محلي أو من HDFS حسب المسار اللي تعطيه)
        JavaRDD<String> lines = sc.textFile(inputPath);

        JavaPairRDD<String, Integer> counts = lines
                .flatMap(s -> Arrays.asList(s.split("\\s+")).iterator())
                .mapToPair(word -> new Tuple2<>(word, 1))
                .reduceByKey(Integer::sum);

        counts.saveAsTextFile(outputDir);

        sc.close();
    }
}
