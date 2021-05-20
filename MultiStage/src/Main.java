import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class Main {

    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new FileReader(new File(GenerateData.BUCKETS_FILE_PATH)));
        List<List<String>> countList = new ArrayList<>();
        while (bufferedReader.ready()) {
            String[] str = bufferedReader.readLine().split(" ");
            List<String> lis = Arrays.stream(str).collect(Collectors.toList());

            countList.add(new ArrayList<>(lis));
        }

        MultiStage multiStage = new MultiStage(countList);
        List<String> l = multiStage.analyze();
        l.forEach(System.out::println);
    }
}
