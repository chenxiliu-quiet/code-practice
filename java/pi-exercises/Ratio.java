public class Ratio {
    public static void main(String[] args) {
        int boy = 20, girl = 30;
        int sum = boy + girl;

        System.out.println("boy / sum             = " + (boy / sum));
        System.out.println("(double)(boy/sum)     = " + (double) (boy / sum) + "     <-- your version (wrong)");
        System.out.println("(double) boy / sum    = " + (double) boy / sum + "   <-- ratio 0~1");
        System.out.println("boy * 100.0 / sum     = " + boy * 100.0 / sum + "    <-- percentage 0~100");
        System.out.println();

        double p1 = boy * 100.0 / sum;
        double p2 = girl * 100.0 / sum;
        try {
            System.out.printf("%.2f ", p1 + "%.2f", p2);
        } catch (Exception e) {
            System.out.println("your printf line -> " + e.getClass().getSimpleName() + ": " + e.getMessage());
        }
        System.out.printf("fixed  -> %.2f %.2f%n", p1, p2);
        System.out.println();
        System.out.println("other example: boy=1 girl=2");
        int b = 1, g = 2, s = b + g;
        System.out.println("  (double)(b/s)  = " + (double) (b / s));
        System.out.println("  b * 100.0 / s  = " + String.format("%.2f", b * 100.0 / s));
        System.out.println("  g * 100.0 / s  = " + String.format("%.2f", g * 100.0 / s));
    }
}
