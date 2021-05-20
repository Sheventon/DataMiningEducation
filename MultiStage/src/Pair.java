public class Pair {
    private int first;
    private int second;
    private int count = 0;

    public Pair(int x, int y) {
        this.first = x;
        this.second = y;
    }

    public int getFirst() {
        return first;
    }

    public int getSecond() {
        return second;
    }

    public int getCount() {
        return count;
    }

    public void setCount(int count) {
        this.count = count;
    }
}
