public class Num {
    public static void main(String[] args) {
        double[] vs = {3.14159, 1.0/3, 0.1 + 0.2, 2.0/3, 0.00001, 0.0001, 10000000.0, 123456789.0, 6283.18, 0.1};
        System.out.printf("%-24s %-26s %s%n", "print(v)", "printf(\"%f\", v)", "printf(\"%.5f\", v)");
        for (double v : vs) {
            System.out.printf("%-24s %-26s %s%n", Double.toString(v), String.format("%f", v), String.format("%.5f", v));
        }
        System.out.println();
        System.out.println("5/2   = " + (5 / 2));
        System.out.println("5.0/2 = " + (5.0 / 2));
        System.out.println("0.1+0.2 == 0.3 ? " + (0.1 + 0.2 == 0.3));
    }
}
