public class GreatestCommonDenominator {


    public double gcd(double a, double b) {
        if (b == 0)
            return a;
        else
            return gcd(b, a % b);
    }

    public double lcm(double a, double b) {
        return Math.abs(a * b) / gcd(a, b);
    }


    public static void main(String[] args) {
        System.out.println(new GreatestCommonDenominator().lcm(4, 3));
    }
}
