public class Money {
    static void show(double y) {
        int cents = (int) Math.round(y * 100);
        System.out.printf("?? %-7.2f -> ?=%-6d 10?%d 5?%d 1?%d 5?%d 1?%d 2?%d 1?%d%n",
            y, cents, cents / 1000, cents % 1000 / 500, cents % 500 / 100,
            cents % 100 / 50, cents % 50 / 10, cents % 10 / 2, cents % 10 % 2);
    }
    public static void main(String[] args) {
        double[] ys = {12.34, 0.99, 10.00, 65.43, 0.29, 8.88};
        for (double y : ys) show(y);
        System.out.println();
        System.out.println("????: 0.29 * 100 = " + (0.29 * 100));
        System.out.println("  (int)(0.29 * 100)        = " + (int) (0.29 * 100) + "   <-- ? 1 ?");
        System.out.println("  Math.round(0.29 * 100)   = " + Math.round(0.29 * 100) + "    <-- ??");
        System.out.println("????: 0.07 * 100 = " + (0.07 * 100));
        System.out.println("????: 12.34 * 100 = " + (12.34 * 100));
        System.out.println("????: 1.15 * 100 = " + (1.15 * 100));
    }
}
