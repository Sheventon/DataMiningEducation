import java.util.*;

public class MultiStage {

    private List<List<Integer>> list;
    private Map<Integer, Integer> hashMap;
    private Map<String, Integer> map;
    private Map<Integer, String> mapString;

    private static final int SUPPORT = 40;

    public MultiStage(List<List<String>> list) {
        hashMap = new HashMap<>();
        map = new HashMap<>();
        mapString = new HashMap<>();
        this.list = listInitialization(list);
    }

    public List<List<Integer>> listInitialization(List<List<String>> list) {
        int k = 1;
        List<List<Integer>> answerList = new ArrayList<>();

        for (List<String> a : list) {
            for (String str : a) {
                if (!map.containsKey(str)) {
                    map.put(str, k);
                    mapString.put(k, str);
                    k++;
                }
                if (!hashMap.containsKey(map.get(str))) {
                    hashMap.put(map.get(str), 0);
                }
                int count = hashMap.get(map.get(str));
                hashMap.remove(map.get(str));
                hashMap.put(map.get(str), count + 1);
            }
        }

        for (List<String> a : list) {
            List<Integer> localList = new ArrayList<>();
            for (String str : a) {
                localList.add(map.get(str));
            }
            answerList.add(localList);
        }
        return answerList;
    }

    public List<String> analyze() {
        List<Pair> doublePairs = multiStage();
        List<String> answerString = new ArrayList<>();
        for (int i = 1; i <= hashMap.size(); i++) {
            if (hashMap.get(i) >= SUPPORT) {
                String str = mapString.get(i);
                answerString.add(str);
            }
        }

        for (Pair pair : doublePairs) {
            String str = mapString.get(pair.getFirst()) + " " + mapString.get(pair.getSecond());
            answerString.add(str);
        }
        return answerString;
    }

    public List<Pair> multiStage() {
        List<Pair> pairList = new ArrayList<>();
        for (List<Integer> list : list) {
            for (int i = 0; i < list.size(); i++) {
                for (int j = i + 1; j < list.size(); j++) {
                    pairList.add(new Pair(list.get(i), list.get(j)));
                }
            }
        }

        List<Set<Pair>> list = integerListMap(pairList, hashMap.size(), 1, 1);
        List<Pair> currentParList = getGoodPair(list, pairList);
        list = integerListMap(currentParList, hashMap.size(), 1, 2);
        currentParList = getGoodPair(list, pairList);
        List<Pair> answerList = new ArrayList<>();
        Set<Pair> answerSet = new HashSet<>();

        for (Pair pair : currentParList) {
            int x = hashMap.get(pair.getFirst());
            int y = hashMap.get(pair.getSecond());
            if (!(x < SUPPORT || y < SUPPORT)) {
                if (answerSet.stream().noneMatch(k -> k.getFirst() == pair.getFirst() && k.getSecond() == pair.getSecond())) {
                    answerSet.add(pair);
                    answerList.add(pair);
                }
            }
        }
        return answerList;
    }

    private List<Pair> getGoodPair(List<Set<Pair>> list, List<Pair> pairList) {
        Set<Pair> goodPairs = new HashSet<>();
        List<Pair> currentParList = new ArrayList<>();
        for (Set<Pair> pairs : list) {
            Iterator<?> iterator = pairs.iterator();
            int currentSum = 0;
            while (iterator.hasNext()) {
                Pair pair = (Pair) iterator.next();
                currentSum += pair.getCount();
            }
            if (currentSum >= SUPPORT) {
                goodPairs.addAll(pairs);
            }
        }

        for (Pair pair : pairList) {
            if (goodPairs.stream().anyMatch(k -> k.getFirst() == pair.getFirst() && k.getSecond() == pair.getSecond())) {
                currentParList.add(pair);
            }
        }
        return currentParList;
    }

    public List<Set<Pair>> integerListMap(List<Pair> list, int hash, int cofFirst, int cofSecond) {
        List<Set<Pair>> answerList = new ArrayList<>();
        for (int i = 0; i < hash; i++) {
            answerList.add(new HashSet<>());
        }
        for (Pair pair : list) {
            int hashPair = (cofFirst * pair.getFirst() + cofSecond * pair.getSecond()) % hash;
            Iterator<?> iterator = answerList.get(hashPair).iterator();
            int k = 0;
            while (iterator.hasNext()) {
                Pair pairNext = (Pair) iterator.next();
                if (pairNext.getFirst() == pair.getFirst() && pairNext.getSecond() == pair.getSecond()) {
                    k = pairNext.getCount();
                }
            }
            answerList.get(hashPair).removeIf(key -> key.getFirst() == pair.getFirst() && key.getSecond() == pair.getSecond());
            pair.setCount(k + 1);
            answerList.get(hashPair).add(pair);
        }
        return answerList;
    }
}
