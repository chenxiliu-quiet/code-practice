public class Fmt {
    public static void main(String[] args) {
        double[][] cs = {{1,1},{2,3},{2.5,8},{3.5,12.25},{10,20},{1.25,4.75}};
        System.out.printf("%-6s%-8s%-24s%s%n", "r", "h", "print(v) =", "printf(\"%.5f\", v) =");
        for (double[] c : cs) {
            double v = c[0] * c[0] * 3.14159 * c[1];
            System.out.printf("%-6.2f%-8.2f%-24s%s   %s%n", c[0], c[1],
                Double.toString(v), String.format("%.5f", v),
                (Double.toString(v).equals(String.format("%.5f", v)) ? "same" : "DIFF"));
        }
    }
}
