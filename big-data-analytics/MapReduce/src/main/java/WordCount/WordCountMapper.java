package WordCount;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class WordCountMapper extends Mapper<Object, Text, Text, IntWritable> {

	private final static IntWritable one = new IntWritable(1);
	private Text word = new Text();

	protected void map(Object key, Text value, Context context) throws IOException, InterruptedException {

		StringTokenizer tokenizer = new StringTokenizer(value.toString());
		while (tokenizer.hasMoreTokens()) {
			String token = tokenizer.nextToken().toLowerCase();
			token = token.replaceAll("'", "");
			token = token.replaceAll("[^a-zA-Z]", "");
			if (token.isEmpty()) continue;
			word.set(token);
			context.write(word, one);
		}
	}
}
