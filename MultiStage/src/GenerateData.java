import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class GenerateData {

    private static final int MAX_COUNT_IN_BUCKET = 10;
    private static final int MIN_COUNT_IN_BUCKET = 3;
    private static final int BUCKETS_COUNT = 500;
    private static final int ITEMS_COUNT = 100;
    public static final String PRODUCTS_FILE_PATH = "src/items.txt";
    public static final String BUCKETS_FILE_PATH = "src/buckets.txt";

    public static void main(String[] args) throws IOException {
        generateItems(ITEMS_COUNT);
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(new File(BUCKETS_FILE_PATH)));
        BufferedReader bufferedReader = new BufferedReader(new FileReader(new File(PRODUCTS_FILE_PATH)));
        List<String> list = new ArrayList<>();
        while (bufferedReader.ready()) {
            String str = bufferedReader.readLine();
            list.add(str);
        }

        for (int i = 0; i < BUCKETS_COUNT; i++) {
            int dia = randomValue(MAX_COUNT_IN_BUCKET, MIN_COUNT_IN_BUCKET);
            for (int j = 0; j < dia; j++) {
                int id = randomValue(list.size() - 1, 0);
                //if (!list.contains(list.get(id)))
                bufferedWriter.write(list.get(id) + " ");
            }
            bufferedWriter.write("\n");
        }
        bufferedWriter.flush();
    }

    public static int randomValue(int max, int min) {
        return (int) (Math.random() * (max - min) + min);
    }

    public static void generateItems(int count) throws IOException {
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(new File(PRODUCTS_FILE_PATH)));
        String[] randomStrings = new String[count];
        Random random = new Random();
        for (int i = 0; i < count; i++) {
            char[] word = new char[random.nextInt(8) + 3];
            for (int j = 0; j < word.length; j++) {
                word[j] = (char) ('a' + random.nextInt(26));
            }
            randomStrings[i] = new String(word);
            bufferedWriter.write(randomStrings[i] + "\n");
        }
        bufferedWriter.close();
    }
}

