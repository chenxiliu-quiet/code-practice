public class PiDiff {
    public static void main(String[] args) {
        double[][] cs = {{1,1},{2,3},{2.5,8},{10,20},{3.5,12.25},{100,50}};
        double[] pis = {3.14, 3.14159, 3.1415926, Math.PI};
        String[] names = {"3.14","3.14159","3.1415926","Math.PI"};
        System.out.printf("%-8s%-8s", "r", "h");
        for (String n : names) System.out.printf("%-14s", n);
        System.out.println();
        for (double[] c : cs) {
            System.out.printf("%-8.2f%-8.2f", c[0], c[1]);
            for (double p : pis) System.out.printf("%-14.5f", p*c[0]*c[0]*c[1]);
            System.out.println();
        }
        System.out.println();
        double[][] oc = {{1.7,3.3},{2.9,7.7},{123.456,7.89},{0.001,99999}};
        for (double[] c : oc) {
            double v1 = c[0]*c[0]*3.14159*c[1];
            double v2 = 3.14159*c[0]*c[0]*c[1];
            System.out.printf("a=%-10.4f b=%-10.4f student=%.5f  reorder=%.5f  %s%n", c[0], c[1], v1, v2, (v1==v2?"same":"DIFF"));
        }
    }
}
