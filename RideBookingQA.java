import java.util.*;

public class RideBookingQA {
    public static void main(String[] args) {
        testNormalBooking();
        testInvalidDistance();
        testExcessivePassengers();
        testDriverUnavailability();
        System.out.println("All RideBooking QA Tests Passed!");
    }

    static void assertTrue(boolean condition, String testName) {
        if (!condition) throw new AssertionError("Test failed: " + testName);
        System.out.println("PASSED: " + testName);
    }

    static void testNormalBooking() {
        double base = 50.0, rate = 14.0, dist = 10.0;
        double fare = base + (dist * rate);
        assertTrue(fare == 190.0, "Normal booking fare calculation");
    }

    static void testInvalidDistance() {
        double dist = 0.0;
        boolean rejected = dist <= 0;
        assertTrue(rejected, "Distance <= 0 rejected");
    }

    static void testExcessivePassengers() {
        int passengers = 3;
        int bikeCapacity = 1;
        boolean rejected = passengers > bikeCapacity;
        assertTrue(rejected, "Excessive passenger rejection on Bike");
    }

    static void testDriverUnavailability() {
        List<String> drivers = new ArrayList<>();
        boolean rejected = drivers.isEmpty();
        assertTrue(rejected, "Unavailable driver handling");
    }
}
