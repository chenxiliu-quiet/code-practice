public class Cyl {
    public static void main(String[] args) {
        double r = 5.5;
        System.out.println("Math.PI * r * r      = " + (Math.PI * r * r));
        System.out.println("r * r * Math.PI      = " + (r * r * Math.PI));
        System.out.println("Math.PI * (r * r)    = " + (Math.PI * (r * r)));
        System.out.println("area * length        = " + (Math.PI * r * r * 12.0));
        System.out.printf ("volume %%.1f          = %.1f%n", Math.PI * r * r * 12.0);
    }
}
