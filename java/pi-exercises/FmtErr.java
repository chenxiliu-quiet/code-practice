public class FmtErr {
    static void t(String label, Runnable r) {
        try { r.run(); System.out.println(); }
        catch (Exception e) { System.out.println(label + "  ->  " + e.getClass().getSimpleName() + ": " + e.getMessage()); }
    }
    public static void main(String[] args) {
        t("printf(\"%f\", \"abc\")      ", () -> System.out.printf("%f", "abc"));
        t("printf(\"%.2f\", \"12.34\")   ", () -> System.out.printf("%.2f", "12.34"));
        t("printf(\"%f\", 3)            ", () -> System.out.printf("%f", 3));
        t("printf(\"%f\", 3L)           ", () -> System.out.printf("%f", 3L));
        t("printf(\"%d\", 3.0)          ", () -> System.out.printf("%d", 3.0));
        t("printf(\"%d\", \"abc\")       ", () -> System.out.printf("%d", "abc"));
        t("printf(\"%c\", \"abc\")       ", () -> System.out.printf("%c", "abc"));
        System.out.println();
        System.out.println("?????: " + String.format("%.2f", 3.14159) + " / " + String.format("%d", 42) + " / " + String.format("%s", 3.14));
        System.out.println("%% ??: " + String.format("50%%"));
    }
}
