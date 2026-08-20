import datetime

class RideBooking:
    VEHICLE_CAPACITY = {"Bike": 1, "Sedan": 4, "SUV": 6, "Premium": 4}
    BASE_FARES = {"Bike": 20.0, "Sedan": 50.0, "SUV": 80.0, "Premium": 120.0}
    RATE_PER_KM = {"Bike": 8.0, "Sedan": 14.0, "SUV": 20.0, "Premium": 30.0}

    def __init__(self, drivers=None):
        self.drivers = drivers or {
            "Bike": ["D_Bike_1"],
            "Sedan": ["D_Sedan_1"],
            "SUV": ["D_SUV_1"],
            "Premium": ["D_Premium_1"]
        }

    def book_ride(self, customer_id, pickup, drop, distance, passengers, vehicle_type, booking_time_str, promo_discount=0.0):
        if distance <= 0:
            return {"status": "REJECTED", "reason": "Invalid distance."}
        if vehicle_type not in self.VEHICLE_CAPACITY:
            return {"status": "REJECTED", "reason": "Invalid vehicle type."}
        if passengers <= 0 or passengers > self.VEHICLE_CAPACITY[vehicle_type]:
            return {"status": "REJECTED", "reason": "Excessive or invalid passenger count."}

        try:
            booking_time = datetime.datetime.strptime(booking_time_str, "%H:%M").time()
        except ValueError:
            return {"status": "REJECTED", "reason": "Invalid booking time format. Use HH:MM."}

        if not self.drivers.get(vehicle_type):
            return {"status": "REJECTED", "reason": "Unavailable drivers for vehicle type."}

        # Calculations
        base = self.BASE_FARES[vehicle_type]
        dist_fare = distance * self.RATE_PER_KM[vehicle_type]
        
        # Peak-hour surcharge (08:00 - 10:00, 17:00 - 20:00)
        peak_surcharge = 0.0
        if (datetime.time(8, 0) <= booking_time <= datetime.time(10, 0)) or \
           (datetime.time(17, 0) <= booking_time <= datetime.time(20, 0)):
            peak_surcharge = dist_fare * 0.25

        # Night surcharge (22:00 - 05:00)
        night_surcharge = 0.0
        if booking_time >= datetime.time(22, 0) or booking_time <= datetime.time(5, 0):
            night_surcharge = dist_fare * 0.30

        # Passenger surcharge for Sedan/SUV extra load
        passenger_surcharge = 20.0 * (passengers - 1) if passengers > 1 else 0.0

        subtotal = base + dist_fare + peak_surcharge + night_surcharge + passenger_surcharge
        discount_amount = min(subtotal, promo_discount)
        final_fare = round(subtotal - discount_amount, 2)

        assigned_driver = self.drivers[vehicle_type].pop(0)
        return {
            "status": "APPROVED",
            "customer_id": customer_id,
            "driver": assigned_driver,
            "final_fare": final_fare,
            "breakdown": {
                "base": base,
                "distance": dist_fare,
                "peak": peak_surcharge,
                "night": night_surcharge,
                "passenger": passenger_surcharge,
                "discount": discount_amount
            }
        }
